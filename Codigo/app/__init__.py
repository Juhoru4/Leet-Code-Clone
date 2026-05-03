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

    # Registrar blueprints en el factory para que existan en app real y tests.
    from routes.ejecucion_endpoint import ejecucion_bp
    app.register_blueprint(ejecucion_bp)

    return app
