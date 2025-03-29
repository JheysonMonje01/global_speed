from app.models.role import Role
from app.models.permission import Permission
from app.utils.database import db

class RoleService:
    @staticmethod
    def get_all_roles():
        """Obtener todos los roles"""
        return [role.to_dict() for role in Role.query.all()]

    @staticmethod
    def create_role(data):
        """Crear un nuevo rol"""
        name = data.get("name")
        description = data.get("description", "")

        if Role.query.filter_by(name=name).first():
            return {"error": "Role already exists"}, 400

        role = Role(name=name, description=description)
        db.session.add(role)
        db.session.commit()

        return {"message": "Role created successfully", "role_id": role.id_rol}, 201

    @staticmethod
    def assign_permissions(role_id, permissions):
        """Asignar permisos a un rol"""
        role = Role.query.get(role_id)
        if not role:
            return {"error": "Role not found"}, 404

        role.permissions = Permission.query.filter(Permission.id_permission.in_(permissions)).all()
        db.session.commit()
        return {"message": "Permissions assigned successfully"}, 200
    
    
    