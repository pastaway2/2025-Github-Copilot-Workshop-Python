"""Main web routes and basic timer APIs."""
from __future__ import annotations

from typing import Any, Dict

from flask import Blueprint, current_app, jsonify, render_template, request

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index() -> str:
    """Render the home page with the current timer snapshot."""
    timer_service = _get_timer_service()
    session_service = _get_session_service()

    status = timer_service.get_status()
    stats = session_service.get_today_statistics()

    context = {
        "title": "ポモドーロタイマー",
        "status": _status_label(status["state"], status["session_type"]),
        "display_time": _format_mmss(status["remaining_seconds"]),
        "completed_sessions": stats["completed_sessions"],
        "display_focus_time": stats["display_focus_time"],
    }
    return render_template("index.html", **context)


@main_bp.post("/api/timer/start")
def start_timer():
    """Start the timer."""
    timer_service = _get_timer_service()
    payload = request.get_json(silent=True) or {}
    session_type = payload.get("session_type", "work")

    try:
        started = timer_service.start_timer(session_type=session_type)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    status = _augment_status(timer_service.get_status())
    status["success"] = started
    return jsonify(status)


@main_bp.post("/api/timer/reset")
def reset_timer():
    """Reset the timer to its initial state."""
    timer_service = _get_timer_service()
    timer_service.reset_timer()
    return jsonify(_augment_status(timer_service.get_status()))


@main_bp.get("/api/timer/status")
def timer_status():
    """Return the current timer status."""
    timer_service = _get_timer_service()
    return jsonify(_augment_status(timer_service.get_status()))


@main_bp.get("/api/sessions/today")
def today_sessions():
    """Return today's session statistics."""
    session_service = _get_session_service()
    return jsonify(session_service.get_today_statistics())


def _get_timer_service():
    service = current_app.extensions.get("timer_service")
    if service is None:
        raise RuntimeError("Timer service is not configured")
    return service


def _get_session_service():
    service = current_app.extensions.get("session_service")
    if service is None:
        raise RuntimeError("Session service is not configured")
    return service


def _format_mmss(remaining_seconds: int) -> str:
    minutes, seconds = divmod(max(0, int(remaining_seconds)), 60)
    return f"{minutes:02d}:{seconds:02d}"


def _status_label(state: str, session_type: str) -> str:
    state_map: Dict[str, str] = {
        "idle": "準備中",
        "running": "実行中",
        "paused": "一時停止",
        "completed": "完了",
    }
    session_map: Dict[str, str] = {
        "work": "作業中",
        "short_break": "休憩中",
        "long_break": "長い休憩",
    }

    if state == "running":
        return session_map.get(session_type, "実行中")
    return state_map.get(state, "準備中")


def _augment_status(status: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(status)
    payload["display_time"] = _format_mmss(status["remaining_seconds"])
    payload["status_label"] = _status_label(status["state"], status["session_type"])
    return payload
