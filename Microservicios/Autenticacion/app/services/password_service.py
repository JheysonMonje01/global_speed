from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from app.utils.database import db
from app.models.user import User
from app.models.password_reset import PasswordReset
from app.utils.email_sender import EmailSender
from werkzeug.security import generate_password_hash

class PasswordService:



    @staticmethod
    def request_password_reset(email):
        user = User.query.filter_by(email=email).first()

        if user:
            serializer = URLSafeTimedSerializer(current_app.config["JWT_SECRET_KEY"])
            token = serializer.dumps(email, salt="password-reset-salt")

            expires_at = datetime.utcnow() + timedelta(
                minutes=current_app.config["PASSWORD_RESET_TOKEN_EXPIRY_MINUTES"]
            )

            reset_request = PasswordReset(user_id=user.id_user, token=token, expires_at=expires_at)
            db.session.add(reset_request)
            db.session.commit()

            reset_link = f"http://localhost:3000/reset-password?token={token}"
            email_body = f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_link}"

            EmailSender.send_email(
                to_email=email,
                subject="Recuperación de Contraseña",
                body=email_body
            )

        # Respuesta genérica, siempre igual
        return {
            "message": "Si este correo electrónico existe en nuestro sistema, recibirás un enlace para restablecer la contraseña en breve."
        }, 200




    @staticmethod
    def reset_password(token, new_password):
        serializer = URLSafeTimedSerializer(current_app.config["JWT_SECRET_KEY"])

        try:
            email = serializer.loads(
                token,
                salt="password-reset-salt",
                max_age=current_app.config["PASSWORD_RESET_TOKEN_EXPIRY_MINUTES"] * 60
            )
        except Exception:
            return {"error": "Token inválido o expirado"}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {"error": "Usuario no encontrado"}, 404

        user.password_hash = generate_password_hash(new_password)

        PasswordReset.query.filter_by(token=token).delete()
        db.session.commit()

        return {"message": "Contraseña restablecida exitosamente."}, 200
