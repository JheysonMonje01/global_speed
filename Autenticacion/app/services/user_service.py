from app.models.user import User
from app.models.role import Role
from app.utils.database import db

class UserService:

    @staticmethod
    def get_all_users(filters=None):
        query = User.query
        if filters:
            if "role_id" in filters:
                query = query.join(User.roles).filter(Role.id_rol == filters["role_id"])
            if "search" in filters:
                search_term = f"%{filters['search']}%"
                query = query.filter((User.username.ilike(search_term)) | (User.email.ilike(search_term)))

        users = query.order_by(User.username.asc()).all()
        return [u.to_dict() for u in users]

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        if "username" in data:
            user.username = data["username"]
        if "email" in data:
            user.email = data["email"]
        if "role_id" in data:
            role = Role.query.get(data["role_id"])
            if not role:
                return {"error": "Role not found"}, 400
            user.roles = [role]  # ✅ Relación many-to-many

        db.session.commit()
        return {"message": "User updated successfully"}, 200

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404

        user.roles.clear()
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
