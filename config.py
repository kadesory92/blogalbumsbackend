import os


class Config:
    """Basic configuration for the application."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    # CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')


class DevelopmentConfig(Config):
    """Configuration for development."""
    FLASK_ENV = 'development'
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production."""
    FLASK_ENV = 'production'
    DEBUG = False
