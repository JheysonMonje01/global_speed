from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.utils.database import db
from app.utils.redis_client import redis_client
from app.security.password import verify_password, hash_password

class AuthService:
    @staticmethod
    def login(data):
        """Autenticación del usuario y generación de JWT"""
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(password, user.password_hash):
            if user:
                user.failed_login_attempts += 1
                db.session.commit()
            return {"error": "Invalid credentials"}, 401

        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()
            return {"error": "Too many failed attempts. Account locked for 30 minutes."}, 403

        if user.locked_until and user.locked_until > datetime.utcnow():
            return {"error": "Account is temporarily locked. Try again later."}, 403

        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        db.session.commit()

        access_token = create_access_token(identity=str(user.id_user), expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=str(user.id_user), expires_delta=timedelta(days=7))



        redis_client.set(f"user_refresh_token_{user.id_user}", refresh_token, ex=604800)  # 7 días

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id_user
        }, 200

    @staticmethod
    def register(data):
        """Registro de un nuevo usuario con rol predeterminado"""
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 400

        hashed_password = hash_password(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        # Asignar el rol predeterminado
        default_role = Role.query.filter_by(name="user").first()
        if default_role:
            new_user.roles.append(default_role)
            db.session.commit()

        return {"message": "User registered successfully"}, 201

    @staticmethod
    def logout(user_id):
        """Cerrar sesión eliminando el Refresh Token del usuario en Redis"""
        redis_client.delete(f"user_refresh_token_{user_id}")
        return {"message": "User logged out successfully"}, 200





    @staticmethod
    def get_all_permissions():
        """Obtener todos los permisos disponibles"""
        permissions = Permission.query.all()
        return [{"id": p.id_permission, "name": p.name, "description": p.description} for p in permissions]


    @staticmethod
    def assign_permission_to_user(user_id, permission_id):
        """Asignar un permiso específico a un usuario"""
        user = User.query.get(user_id)
        permission = Permission.query.get(permission_id)

        if not user:
            return {"error": "User not found"}, 404
        if not permission:
            return {"error": "Permission not found"}, 404

        user.permissions.append(permission)
        db.session.commit()
        return {"message": "Permission assigned successfully"}, 200


    @staticmethod
    def create_permission(data):
        """Crear un nuevo permiso"""
        name = data.get("name")
        description = data.get("description", "")

        if Permission.query.filter_by(name=name).first():
            return {"error": "Permission already exists"}, 400

        permission = Permission(name=name, description=description)
        db.session.add(permission)
        db.session.commit()

        return permission.to_dict(), 201

    @staticmethod
    def delete_permission(permission_id):
        """Eliminar un permiso"""
        permission = Permission.query.get(permission_id)
        if not permission:
            return {"error": "Permission not found"}, 404

        db.session.delete(permission)
        db.session.commit()
        return {"message": "Permission deleted successfully"}, 200



