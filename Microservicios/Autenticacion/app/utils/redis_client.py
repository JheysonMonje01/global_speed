import redis
import logging
import time

logger = logging.getLogger("auth_microservice")
redis_client = None

def init_redis(app, max_retries=5, retry_delay=3):
    global redis_client
    redis_url = app.config.get("REDIS_URL", "redis://redis:6379/0")

    for attempt in range(max_retries):
        try:
            client = redis.Redis.from_url(redis_url, decode_responses=True)

            if client.ping():
                redis_client = client
                logger.info("✅ Redis conectado correctamente.")
                return redis_client

        except Exception as e:
            logger.error(f"⚠ Error al conectar Redis (intento {attempt+1}/{max_retries}): {e}")
        
        time.sleep(retry_delay)

    redis_client = None
    logger.critical("❌ No se pudo conectar a Redis después de varios intentos. Algunas funcionalidades pueden fallar.")
