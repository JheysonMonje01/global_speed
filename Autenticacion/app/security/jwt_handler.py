from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
from datetime import timedelta
from app.utils.redis_client import redis_client
import logging

jwt = JWTManager()
logger = logging.getLogger("auth_microservice")

def init_jwt(app):
    """Inicializa JWT en la aplicación Flask"""
    jwt.init_app(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """Verifica si el token ha sido revocado en Redis"""
    jti = jwt_payload["jti"]

    if redis_client is None:
        logger.warning("⚠ Advertencia: Redis no está conectado. No se puede verificar si el token fue revocado.")
        return False  # Permitir la autenticación si Redis no está disponible

    try:
        return redis_client.exists(f"revoked_token_{jti}") == 1
    except Exception as e:
        logger.error(f"❌ Error al consultar Redis: {e}")
        return False  # Evitar errores críticos

def generate_tokens(user_id):
    """Genera tokens de acceso y refresco"""
    access_token = create_access_token(identity=str(user_id), expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(identity=str(user_id), expires_delta=timedelta(days=7))
    return access_token, refresh_token

def revoke_token(jti, expires_in=3600):
    """Revoca un token agregándolo a Redis"""
    if redis_client is not None:
        try:
            redis_client.set(f"revoked_token_{jti}", "true", ex=expires_in)
        except Exception as e:
            logger.error(f"❌ Error al revocar el token en Redis: {e}")
    else:
        logger.error("❌ Error: Redis no disponible, no se puede revocar el token.")
