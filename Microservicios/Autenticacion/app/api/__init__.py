from flask import Blueprint

# Crear Blueprints vacíos (para evitar importaciones circulares)
auth_bp = Blueprint("auth", __name__)
users_bp = Blueprint("users", __name__)
roles_bp = Blueprint("roles", __name__)
password_bp = Blueprint("password", __name__)  # ✅ Nuevo Blueprint para contraseñas


# Importar vistas después de definir los Blueprints
from app.api import auth, users, roles, password

# Asignar los Blueprints correctamente
auth_bp = auth.auth_bp
users_bp = users.users_bp
roles_bp = roles.roles_bp
password_bp = password.password_bp  # ✅ Registrar aquí el nuevo Blueprint