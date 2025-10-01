"""Abstract repository interfaces for session persistence."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List

from models.session import PomodoroSession, DailyStatistics


class SessionRepositoryInterface(ABC):
    """Interface for session persistence operations."""

    @abstractmethod
    def save(self, session: PomodoroSession) -> PomodoroSession:
        """Persist a session and return the stored instance."""

    @abstractmethod
    def get_by_date(self, target_date: date) -> List[PomodoroSession]:
        """Return sessions for the provided date."""

    @abstractmethod
    def get_completed_sessions_count(self, target_date: date) -> int:
        """Return number of completed sessions for the provided date."""

    @abstractmethod
    def get_total_focus_time(self, target_date: date) -> int:
        """Return aggregated focus time in seconds for the date."""

    @abstractmethod
    def get_daily_statistics(self, target_date: date) -> DailyStatistics:
        """Return aggregated statistics for the date."""
