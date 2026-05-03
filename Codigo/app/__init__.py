from flask import Flask
from .extensions import db
import os
from dotenv import load_dotenv
from routes.problems import problems_bp

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SESSION_POOLER_URL",
        os.getenv("DATABASE_URL", "sqlite:///test.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(problems_bp)

    return app
