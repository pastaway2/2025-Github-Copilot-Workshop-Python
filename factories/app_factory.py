"""Application factory for the Pomodoro timer."""
from __future__ import annotations

from pathlib import Path

from flask import Flask
from flask_socketio import SocketIO

from config import get_config
from interfaces.clock import SystemClock
from interfaces.events import EventEmitter
from models.timer import TimerConfig
from repositories.memory_repository import MemorySessionRepository
from routes.main import main_bp
from services.session_service import SessionService
from services.timer_service import TimerService

BASE_DIR = Path(__file__).resolve().parent.parent

socketio = SocketIO()


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )

    config_class = get_config(config_name)
    app.config.from_object(config_class)
    config_class.init_app(app)

    socketio.init_app(
        app,
        async_mode=app.config.get("SOCKETIO_ASYNC_MODE", "threading"),
        cors_allowed_origins=app.config.get("SOCKETIO_CORS_ALLOWED_ORIGINS", []),
    )

    _register_dependencies(app)

    register_blueprints(app)

    return app


def register_blueprints(app: Flask) -> None:
    """Register application blueprints."""
    app.register_blueprint(main_bp)


def _register_dependencies(app: Flask) -> None:
    """Setup application-wide dependencies."""
    clock = SystemClock()
    event_emitter = EventEmitter()
    session_repository = MemorySessionRepository()
    session_service = SessionService(session_repository, clock)

    timer_config = TimerConfig(
        work_duration=app.config.get("TIMER_WORK_DURATION", 25 * 60),
        short_break_duration=app.config.get("TIMER_SHORT_BREAK", 5 * 60),
        long_break_duration=app.config.get("TIMER_LONG_BREAK", 15 * 60),
        sessions_until_long_break=app.config.get("TIMER_SESSIONS_UNTIL_LONG_BREAK", 4),
    )

    timer_service = TimerService(
        config=timer_config,
        clock=clock,
        event_emitter=event_emitter,
        session_service=session_service,
    )

    app.extensions["clock"] = clock
    app.extensions["event_emitter"] = event_emitter
    app.extensions["session_repository"] = session_repository
    app.extensions["session_service"] = session_service
    app.extensions["timer_service"] = timer_service
