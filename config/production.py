"""
Production configuration
"""
import os
from .base import BaseConfig


class ProductionConfig(BaseConfig):
    """Production configuration"""

    DEBUG = False
    TESTING = False

    # Production database (PostgreSQL recommended)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///pomodoro_prod.db'

    # Production secret key (must be set in environment)
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Production SocketIO settings
    SOCKETIO_CORS_ALLOWED_ORIGINS = [origin for origin in os.environ.get('CORS_ORIGINS', '').split(',') if origin]

    # Security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    @staticmethod
    def init_app(app) -> None:
        """Initialize production-specific settings"""
        BaseConfig.init_app(app)

        if not app.config.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable must be set in production")

        # Setup production logging
        import logging
        from logging.handlers import RotatingFileHandler

        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')

            file_handler = RotatingFileHandler(
                'logs/pomodoro.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Pomodoro Timer startup')