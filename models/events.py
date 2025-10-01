"""
Event models (if additional events needed)
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimerStateChanged:
    """Event fired when timer state changes"""
    state: str
    session_type: str
    remaining_seconds: int
    total_seconds: int


@dataclass
class SessionCompleted:
    """Event fired when session is completed"""
    session_id: str
    session_type: str
    duration_seconds: int
    completed: bool = True


@dataclass
class SessionStatisticsUpdated:
    """Event fired when statistics are updated"""
    completed_sessions: int
    total_focus_time_seconds: int


@dataclass
class NotificationEvent:
    """Event for notifications"""
    notification_type: str
    message: str
    session_id: Optional[str] = None
