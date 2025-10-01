"""
Development configuration
"""
from .base import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Development database
    DATABASE_URL = 'sqlite:///pomodoro_dev.db'
    
    # Development SocketIO settings
    SOCKETIO_CORS_ALLOWED_ORIGINS = ["http://localhost:5000", "http://127.0.0.1:5000"]
    
    # Logging
    LOG_LEVEL = 'DEBUG'
    
    @staticmethod
    def init_app(app) -> None:
        """Initialize development-specific settings"""
        BaseConfig.init_app(app)
        
        # Setup development logging
        import logging
        logging.basicConfig(level=logging.DEBUG)