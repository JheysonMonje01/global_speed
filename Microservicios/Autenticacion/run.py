from app import create_app
import logging

app = create_app()

if __name__ == "__main__":
    try:
        logging.info("🚀 Iniciando el microservicio de autenticación...")
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        logging.critical(f"❌ Error crítico al iniciar la aplicación: {e}")
