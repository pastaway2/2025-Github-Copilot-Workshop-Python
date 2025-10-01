"""Session management service."""
from __future__ import annotations

from datetime import date
from typing import Optional, Dict, Any
from uuid import uuid4

from interfaces.clock import ClockInterface
from models.session import PomodoroSession
from repositories.base import SessionRepositoryInterface


class SessionService:
    """Manage creation and persistence of Pomodoro sessions."""

    def __init__(self, repository: SessionRepositoryInterface, clock: ClockInterface) -> None:
        self._repository = repository
        self._clock = clock
        self._current_session: Optional[PomodoroSession] = None

    def start_session(self, session_type: str = "work") -> str:
        """Start a new session if one isn't already active."""
        if self._current_session and not self._current_session.completed:
            return self._current_session.session_id

        session = PomodoroSession(
            session_id=str(uuid4()),
            session_type=session_type,
            start_time=self._clock.now(),
        )
        self._current_session = session
        return session.session_id

    def complete_current_session(self, duration_seconds: int) -> Optional[PomodoroSession]:
        """Mark the current session as completed and persist it."""
        if not self._current_session:
            return None

        self._current_session.complete(self._clock.now())
        if duration_seconds:
            self._current_session.duration_seconds = duration_seconds
        saved = self._repository.save(self._current_session)
        self._current_session = None
        return saved

    def discard_current_session(self) -> None:
        """Discard the active session without persisting it."""
        self._current_session = None

    def get_today_statistics(self) -> Dict[str, Any]:
        """Return today's statistics with formatted values."""
        today = self._clock.now().date()
        stats = self._repository.get_daily_statistics(today)

        return {
            "completed_sessions": stats.completed_sessions,
            "total_focus_time_seconds": stats.total_focus_time_seconds,
            "display_focus_time": self._format_focus_time(stats.total_focus_time_seconds),
        }

    @staticmethod
    def _format_focus_time(total_seconds: int) -> str:
        if total_seconds <= 0:
            return "0分"
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        parts: list[str] = []
        if hours:
            parts.append(f"{hours}時間")
        if minutes or not parts:
            parts.append(f"{minutes}分")
        return "".join(parts)
