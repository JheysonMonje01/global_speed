from app.utils.database import db
from datetime import datetime
from app.models.role_permission import role_permissions  # Importación correcta

class Role(db.Model):
    __tablename__ = "roles"

    id_rol = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    permissions = db.relationship("Permission", secondary=role_permissions, backref="roles")

    def to_dict(self):
        return {
            "id_rol": self.id_rol,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
