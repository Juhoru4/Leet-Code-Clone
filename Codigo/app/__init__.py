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
        os.getenv("DATABASE_URL", "sqlite:///test.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Auth y ejecución
    try:
        from .auth import bp as auth_bp
        app.register_blueprint(auth_bp)
    except Exception as e:
        print(f"Error registrando auth blueprint: {e}")

    try:
        from routes.ejecucion_endpoint import ejecucion_bp
        app.register_blueprint(ejecucion_bp)
    except Exception as e:
        print(f"Error registrando ejecucion blueprint: {e}")

    # Problemas: UI/listado y detalle/casos
    try:
        from routes.problems import problems_bp as problems_ui_bp
        app.register_blueprint(problems_ui_bp)
    except Exception as e:
        print(f"Error registrando problems ui blueprint: {e}")

    try:
        from services.problemas_blueprint import problems_bp as api_problems_bp
        app.register_blueprint(api_problems_bp, url_prefix="/api/problems")
    except Exception as e:
        print(f"Error registrando api problems blueprint: {e}")

    # Submissions
    try:
        from services.submissions_blueprint import submissions_bp
        app.register_blueprint(submissions_bp, url_prefix="/api/submissions")
    except Exception as e:
        print(f"Error registrando submissions blueprint: {e}")

    return app