"""
Testing configuration
"""
from .base import BaseConfig


class TestingConfig(BaseConfig):
    """Testing configuration"""
    
    DEBUG = False
    TESTING = True
    
    # Fast timers for testing (in seconds)
    TIMER_WORK_DURATION = 5          # 5 seconds for fast tests
    TIMER_SHORT_BREAK = 2            # 2 seconds
    TIMER_LONG_BREAK = 3             # 3 seconds
    TIMER_SESSIONS_UNTIL_LONG_BREAK = 2
    
    # In-memory database for tests
    DATABASE_URL = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Testing SocketIO settings
    SOCKETIO_ASYNC_MODE = 'threading'
    
    @staticmethod
    def init_app(app) -> None:
        """Initialize testing-specific settings"""
        BaseConfig.init_app(app)
        
        # Setup test logging
        import logging
        logging.basicConfig(level=logging.WARNING)