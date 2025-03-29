from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])  # Se corrigió la URL base
@jwt_required()
def get_users():
    """Obtener la lista de usuarios"""
    return jsonify(UserService.get_all_users()), 200

@users_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    """Obtener información de un usuario por ID"""
    response, status = UserService.get_user_by_id(user_id)
    return jsonify(response), status

@users_bp.route("/users/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """Obtener los datos del usuario autenticado"""
    user_id = get_jwt_identity()
    response, status = UserService.get_user_by_id(user_id)
    return jsonify(response), status

@users_bp.route("/users/me", methods=["PUT"])
@jwt_required()
def update_user():
    """Actualizar los datos del usuario autenticado"""
    user_id = get_jwt_identity()
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    response, status = UserService.update_user(user_id, data)
    return jsonify(response), status

@users_bp.route("/users/me", methods=["DELETE"])
@jwt_required()
def delete_user():
    """Eliminar la cuenta del usuario autenticado"""
    user_id = get_jwt_identity()
    response, status = UserService.delete_user(user_id)
    return jsonify(response), status
