from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.utils.redis_client import redis_client

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://redis:6379"
)

def init_limiter(app):
    limiter.init_app(app)

# Límites personalizados para endpoints críticos
login_limiter = limiter.shared_limit("5 per minute", scope="login")
register_limiter = limiter.shared_limit("3 per minute", scope="register")
