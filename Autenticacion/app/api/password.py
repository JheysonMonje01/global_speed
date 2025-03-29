from flask import Blueprint, request, jsonify
from app.services.password_service import PasswordService

password_bp = Blueprint("password", __name__)

@password_bp.route("/forgot", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "El email es obligatorio"}), 400

    response, status = PasswordService.request_password_reset(email)
    return jsonify(response), status

@password_bp.route("/reset", methods=["POST"])
def reset_password():
    data = request.json
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Token y nueva contraseña son obligatorios"}), 400

    response, status = PasswordService.reset_password(token, new_password)
    return jsonify(response), status
