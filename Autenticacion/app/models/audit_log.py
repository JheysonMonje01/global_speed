from app.utils.database import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id_audit = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id_user"))
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id_audit": self.id_audit,
            "user_id": self.user_id,
            "action": self.action,
            "description": self.description,
            "created_at": self.created_at
        }
