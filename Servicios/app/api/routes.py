from flask import Blueprint, request, jsonify
from app.services.pppoe_service import (
    create_pppoe_user,
    list_pppoe_users,
    suspender_pppoe_user,
    activar_pppoe_user
)

pppoe_bp = Blueprint('pppoe', __name__, url_prefix='/pppoe')

@pppoe_bp.route('/create', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    password = data['password']
    create_pppoe_user(username, password)
    return jsonify({"message": "Usuario PPPoE creado exitosamente."}), 201

@pppoe_bp.route('/list', methods=['GET'])
def list_users():
    users = list_pppoe_users()
    return jsonify(users), 200

@pppoe_bp.route('/suspender/<username>', methods=['PUT'])
def suspender_user(username):
    try:
        suspender_pppoe_user(username)
        return jsonify({"message": f"Servicio suspendido para '{username}'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pppoe_bp.route('/activar/<username>', methods=['PUT'])
def activar_user(username):
    try:
        activar_pppoe_user(username)
        return jsonify({"message": f"Servicio activado para '{username}'"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
