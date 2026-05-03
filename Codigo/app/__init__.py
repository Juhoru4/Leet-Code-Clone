from flask import Flask
from .extensions import db
import os
from dotenv import load_dotenv

load_dotenv()


def create_app(database_uri=None):
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "templates"))
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))
    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri or os.getenv(
        "SESSION_POOLER_URL",
        os.getenv("DATABASE_URL")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Registrar blueprints si existen - Supabase Auth
    try:
        from Codigo.app.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
    except Exception:
        pass

    # Registrar blueprints - Ejecución de código
    try:
        from Codigo.routes.ejecucion_endpoint import ejecucion_bp
        app.register_blueprint(ejecucion_bp)
    except Exception:
        pass

    return app
