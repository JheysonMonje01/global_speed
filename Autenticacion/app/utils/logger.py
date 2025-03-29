import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """Configura el logger con rotación de archivos"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger("auth_microservice")
    logger.setLevel(log_level)

    # Consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Archivo con rotación de logs
    file_handler = RotatingFileHandler("logs/app.log", maxBytes=2 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()
