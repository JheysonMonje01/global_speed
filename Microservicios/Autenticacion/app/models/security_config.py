from app.utils.database import db
from datetime import datetime

class SecurityConfiguration(db.Model):
    __tablename__ = "security_configurations"

    id_config = db.Column(db.Integer, primary_key=True)
    max_login_attempts = db.Column(db.Integer, default=5)
    lockout_time_minutes = db.Column(db.Integer, default=30)
    password_reset_token_expiry_minutes = db.Column(db.Integer, default=60)
    password_complexity = db.Column(db.String(100), default="medium")
    session_timeout_minutes = db.Column(db.Integer, default=15)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id_config": self.id_config,
            "max_login_attempts": self.max_login_attempts,
            "lockout_time_minutes": self.lockout_time_minutes,
            "password_reset_token_expiry_minutes": self.password_reset_token_expiry_minutes,
            "password_complexity": self.password_complexity,
            "session_timeout_minutes": self.session_timeout_minutes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
