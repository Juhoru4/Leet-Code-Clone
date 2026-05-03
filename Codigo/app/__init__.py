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

    # Blueprints ya resgistrados 
    try:
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
    except Exception:
        pass

    from services.problemas_blueprint import problems_bp
    from services.submissions_blueprint import submissions_bp
    app.register_blueprint(problems_bp, url_prefix="/api/problems")
    app.register_blueprint(submissions_bp, url_prefix="/api/submissions")

    return app
