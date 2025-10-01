"""In-memory session repository for development and testing."""
from __future__ import annotations

from datetime import date
from typing import Dict, List

from models.session import PomodoroSession, DailyStatistics
from .base import SessionRepositoryInterface


class MemorySessionRepository(SessionRepositoryInterface):
    """Simple in-memory repository using per-day storage."""

    def __init__(self) -> None:
        self._sessions: Dict[str, List[PomodoroSession]] = {}

    def save(self, session: PomodoroSession) -> PomodoroSession:
        key = session.start_time.date().isoformat()
        day_sessions = self._sessions.setdefault(key, [])

        for idx, stored in enumerate(day_sessions):
            if stored.session_id == session.session_id:
                day_sessions[idx] = session
                break
        else:
            day_sessions.append(session)
        return session

    def get_by_date(self, target_date: date) -> List[PomodoroSession]:
        key = target_date.isoformat()
        return list(self._sessions.get(key, []))

    def get_completed_sessions_count(self, target_date: date) -> int:
        return sum(1 for session in self.get_by_date(target_date) if session.completed)

    def get_total_focus_time(self, target_date: date) -> int:
        return sum(
            session.duration_seconds or 0
            for session in self.get_by_date(target_date)
            if session.completed
        )

    def get_daily_statistics(self, target_date: date) -> DailyStatistics:
        stats = DailyStatistics(date=target_date)
        for session in self.get_by_date(target_date):
            if session.completed:
                stats.add_session(session)
        return stats

    def clear(self) -> None:
        """Reset repository contents."""
        self._sessions.clear()
