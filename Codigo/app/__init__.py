from flask import Flask
from .extensions import db
import os
from dotenv import load_dotenv

load_dotenv()


def create_app(database_uri=None):
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
    app = Flask(__name__, template_folder=templates_path)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri or os.getenv(
        "SESSION_POOLER_URL",
        os.getenv("DATABASE_URL")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Blueprints HU-03
    from routes.ejecucion_endpoint import ejecucion_bp
    app.register_blueprint(ejecucion_bp)

    # Blueprints HU-04
    try:
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
    except Exception:
        pass

    from services.problems_blueprint import problems_bp
    from services.submissions_blueprint import submissions_bp
    app.register_blueprint(problems_bp, url_prefix="/api/problems")
    app.register_blueprint(submissions_bp, url_prefix="/api/submissions")
    
    return app
