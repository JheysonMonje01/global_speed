from flask import Flask
from app.api.routes import pppoe_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(pppoe_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
