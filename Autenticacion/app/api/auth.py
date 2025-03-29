from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    """Manejo de inicio de sesión con JWT"""
    data = request.json

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Invalid request. 'email' and 'password' are required"}), 400

    response, status = AuthService.login(data)
    return jsonify(response), status

@auth_bp.route("/register", methods=["POST"])
def register():
    """Registro de nuevos usuarios"""
    data = request.json

    if not data or "username" not in data or "phone" not in data or "email" not in data or "password" not in data:
        return jsonify({"error": "Invalid request. 'username', 'email', 'phone', and 'password' are required"}), 400

    response, status = AuthService.register(data)
    return jsonify(response), status

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Cerrar sesión eliminando el refresh token (sin estado)"""
    user_id = get_jwt_identity()
    response, status = AuthService.logout(user_id)
    return jsonify(response), status

@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Obtener un nuevo Access Token usando el Refresh Token"""
    data = request.json

    if not data or "refresh_token" not in data:
        return jsonify({"error": "Refresh token is required"}), 400

    response, status = AuthService.refresh_token(data["refresh_token"])
    return jsonify(response), status
