from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta
from app.models.user import User
from app.models.role import Role
from app.models.audit_log import AuditLog
from app.utils.database import db
from app.utils.redis_client import redis_client
from app.security.password import verify_password, hash_password

class AuthService:
    @staticmethod
    def login(data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"error": "El correo electrónico y la contraseña son obligatorios."}, 400

        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(password, user.password_hash):
            if user:
                user.failed_login_attempts += 1
                db.session.commit()
            return {"error": "Correo electrónico o contraseña incorrectos."}, 401

        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()
            return {"error": "Demasiados intentos fallidos. Tu cuenta está bloqueada durante 30 minutos."}, 403

        if user.locked_until and user.locked_until > datetime.utcnow():
            return {"error": "Tu cuenta está bloqueada temporalmente. Por favor, inténtalo más tarde."}, 403

        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        db.session.commit()

        user_id_str = str(user.id_user)
        access_token = create_access_token(identity=str(user.id_user), expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=str(user.id_user), expires_delta=timedelta(days=7))

        redis_client.set(f"user_refresh_token_{user.id_user}", refresh_token, ex=604800)

        # Registro en auditoría
        audit = AuditLog(user_id=user.id_user, action="login", description="Usuario inició sesión")
        db.session.add(audit)
        db.session.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id_user
        }, 200

    @staticmethod
    def register(data):
        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        role_id = data.get("role_id", 4)  # Por defecto cliente

        if not all([username, email, phone, password]):
            return {"error": "Todos los campos (usuario, email, teléfono y contraseña) son obligatorios."}, 400

        existing_user = User.query.filter(
            (User.email == email) | (User.phone == phone) | (User.username == username)
        ).first()

        if existing_user:
            if existing_user.email == email:
                return {"error": "El correo electrónico ya está registrado."}, 400
            if existing_user.phone == phone:
                return {"error": "El número de teléfono ya está registrado."}, 400
            if existing_user.username == username:
                return {"error": "El nombre de usuario ya está registrado."}, 400

        hashed_password = hash_password(password)
        new_user = User(username=username, email=email, phone=phone, password_hash=hashed_password)

        role = Role.query.get(role_id)
        if not role:
            return {"error": "Rol no encontrado."}, 400

        new_user.roles.append(role)
        db.session.add(new_user)
        db.session.commit()

        # Registro en auditoría
        audit = AuditLog(user_id=new_user.id_user, action="register", description="Usuario registrado")
        db.session.add(audit)
        db.session.commit()

        return {"message": "Usuario registrado exitosamente", "user_id": new_user.id_user}, 201

    @staticmethod
    def refresh_token(refresh_token):
        try:
            decoded_token = decode_token(refresh_token)
            user_id = decoded_token.get("sub")

            stored_token = redis_client.get(f"user_refresh_token_{user_id}")

            if not stored_token:
                return {"error": "El token de actualización no existe o ha expirado."}, 401

            stored_token_str = stored_token.strip()
            refresh_token_str = refresh_token.strip()

            if stored_token_str != refresh_token_str:
                return {"error": "Token de actualización inválido."}, 401

            new_access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=1))
            return {"access_token": new_access_token}, 200

        except Exception as e:
            return {"error": f"Token inválido: {str(e)}"}, 401

    @staticmethod
    def logout(user_id):
        redis_client.delete(f"user_refresh_token_{user_id}")
        audit = AuditLog(user_id=user_id, action="logout", description="Usuario cerró sesión")
        db.session.add(audit)
        db.session.commit()
        return {"message": "Sesión cerrada correctamente."}, 200
