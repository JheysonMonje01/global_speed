from app.utils.database import db
from datetime import datetime

class PasswordReset(db.Model):
    __tablename__ = "password_resets"

    id_password = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id_password": self.id_password,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at,
            "created_at": self.created_at
        }
