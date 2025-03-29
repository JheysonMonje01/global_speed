from app.utils.database import db

# Tabla intermedia para la relación Many-to-Many entre Usuarios y Roles
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id_user"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id_rol"), primary_key=True)
)
