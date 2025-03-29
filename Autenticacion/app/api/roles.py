from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.role_service import RoleService

# Definir el blueprint para roles
roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_all_roles():
    """Obtener todos los roles."""
    roles = RoleService.get_all_roles()
    return jsonify([role.to_dict() for role in roles]), 200

@roles_bp.route('/roles/<int:role_id>', methods=['GET'])
@jwt_required()
def get_role(role_id):
    """Obtener un rol por su ID."""
    role = RoleService.get_role_by_id(role_id)
    if role:
        return jsonify(role.to_dict()), 200
    return jsonify({"error": "Role not found"}), 404

@roles_bp.route('/roles', methods=['POST'])
@jwt_required()
def create_role():
    """Crear un nuevo rol."""
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Invalid request. 'name' is required"}), 400

    role = RoleService.create_role(data)
    return jsonify(role.to_dict()), 201

@roles_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    """Actualizar un rol existente."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid request. No data provided"}), 400

    role = RoleService.update_role(role_id, data)
    if role:
        return jsonify(role.to_dict()), 200
    return jsonify({"error": "Role not found"}), 404

@roles_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    """Eliminar un rol por su ID."""
    success = RoleService.delete_role(role_id)
    if success:
        return jsonify({"message": "Role deleted"}), 200
    return jsonify({"error": "Role not found"}), 404
