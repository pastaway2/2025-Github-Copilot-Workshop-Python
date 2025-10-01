"""
Base configuration for Pomodoro Timer Application
"""
import os
from typing import Dict, Any


class BaseConfig:
    """Base configuration with common settings"""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Timer settings (in seconds)
    TIMER_WORK_DURATION = 25 * 60        # 25 minutes
    TIMER_SHORT_BREAK = 5 * 60           # 5 minutes  
    TIMER_LONG_BREAK = 15 * 60           # 15 minutes
    TIMER_SESSIONS_UNTIL_LONG_BREAK = 4  # Number of work sessions before long break
    
    # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///pomodoro.db'
    
    # Flask-SocketIO settings
    SOCKETIO_ASYNC_MODE = 'threading'
    SOCKETIO_CORS_ALLOWED_ORIGINS = []
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # Application settings
    TIMEZONE = 'UTC'
    LANGUAGE = 'ja'  # Japanese
    
    @staticmethod
    def init_app(app) -> None:
        """Initialize application with configuration"""
        pass