from flask import Flask, jsonify
from flask_cors import CORS
from app.utils.database import db
from app.security.jwt_handler import init_jwt
from app.security.rate_limiter import init_limiter
from app.utils.redis_client import init_redis, redis_client
from app.utils.email_sender import mail
import logging

def create_app():
    app = Flask(__name__)

    # Cargar configuración desde el archivo config.py
    app.config.from_object('app.config.Config')

    # Inicializar base de datos
    db.init_app(app)

    # Inicializar Redis
    init_redis(app)

    if redis_client is None:
        logging.critical("❌ Redis no está conectado. Algunas funcionalidades pueden fallar.")
    else:
        logging.info("✅ Redis conectado correctamente desde __init__.py")

    # Inicializar JWT y Rate Limiter después de Redis
    init_jwt(app)
    init_limiter(app)

    # Inicializar Flask-Mail
    mail.init_app(app)

    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": ["https://myfrontend.com", "http://localhost:3000"]}})

    # Registrar Blueprints
    from app.api import auth_bp, users_bp, roles_bp, password_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/user')
    app.register_blueprint(roles_bp, url_prefix='/api/roles')
    app.register_blueprint(password_bp, url_prefix='/api/password')

    # Manejo global de errores
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error"}), 500

    # Endpoint para testear Redis
    @app.route("/test_redis")
    def test_redis():
        if redis_client:
            redis_client.set("test_key", "hello redis", ex=60)
            value = redis_client.get("test_key")
            return jsonify({"redis": "conectado", "valor": value}), 200
        else:
            return jsonify({"error": "Redis no conectado"}), 500

    return app
