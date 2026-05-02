import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Cambia a True para ver SQL queries


class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SESSION_POOLER_URL",
        os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:password@localhost:5432/leet_code_db"
        )
    )


class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SESSION_POOLER_URL",
        "postgresql://postgres:password@localhost:5432/leet_code_db"
    )


class TestingConfig(Config):
    """Configuración de testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
