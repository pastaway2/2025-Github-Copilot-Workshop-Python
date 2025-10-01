"""
Session domain models
"""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional


@dataclass
class PomodoroSession:
    """Represents a Pomodoro session"""
    session_id: str
    session_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    completed: bool = False
    notes: Optional[str] = None

    def complete(self, end_time: datetime) -> None:
        """Complete the session"""
        self.end_time = end_time
        self.duration_seconds = int((end_time - self.start_time).total_seconds())
        self.completed = True

    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'session_type': self.session_type,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'completed': self.completed,
            'notes': self.notes,
        }


@dataclass
class DailyStatistics:
    """Daily session statistics"""
    date: date
    completed_sessions: int = 0
    total_focus_time_seconds: int = 0
    sessions: list = field(default_factory=list)

    def add_session(self, session: PomodoroSession) -> None:
        """Add completed session to statistics"""
        if session.completed and session.duration_seconds:
            self.completed_sessions += 1
            self.total_focus_time_seconds += session.duration_seconds
            self.sessions.append(session)

    def to_dict(self) -> dict:
        """Convert statistics to dictionary"""
        return {
            'date': self.date.isoformat(),
            'completed_sessions': self.completed_sessions,
            'total_focus_time_seconds': self.total_focus_time_seconds,
            'sessions': [session.to_dict() for session in self.sessions],
        }
