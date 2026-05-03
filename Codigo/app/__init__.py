from flask import Flask
from .extensions import db
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SESSION_POOLER_URL",
        os.getenv("DATABASE_URL")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Registrar blueprints si existen
    try:
        from Codigo.app.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
    except Exception:
        pass

    return app
