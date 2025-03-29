import routeros_api
from app.config.setting import Config

def connect():
    connection = routeros_api.RouterOsApiPool(
        Config.MIKROTIK_HOST,
        username=Config.MIKROTIK_USER,
        password=Config.MIKROTIK_PASS,
        plaintext_login=True
    )
    return connection
