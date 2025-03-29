from app.utils.database import db
from datetime import datetime
from app.models.user_role import user_roles  # Importación correcta

class User(db.Model):
    __tablename__ = "users"

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)
    locked_until = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    roles = db.relationship("Role", secondary=user_roles, backref="users")

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "is_active": self.is_active,
            "failed_login_attempts": self.failed_login_attempts,
            "locked_until": self.locked_until,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
