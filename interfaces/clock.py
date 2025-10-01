"""
Clock interface for time abstraction
"""
from abc import ABC, abstractmethod
from datetime import datetime
import time


class ClockInterface(ABC):
    """Abstract interface for time operations"""
    
    @abstractmethod
    def now(self) -> datetime:
        """Get current time"""
        pass
    
    @abstractmethod
    def timestamp(self) -> float:
        """Get current timestamp"""
        pass


class SystemClock(ClockInterface):
    """System clock implementation"""
    
    def now(self) -> datetime:
        """Get current system time"""
        return datetime.now()
    
    def timestamp(self) -> float:
        """Get current system timestamp"""
        return time.time()


class MockClock(ClockInterface):
    """Mock clock for testing"""
    
    def __init__(self, initial_time: datetime = None):
        self._current_time = initial_time or datetime.now()
        self._timestamp = self._current_time.timestamp()
    
    def now(self) -> datetime:
        """Get mocked current time"""
        return self._current_time
    
    def timestamp(self) -> float:
        """Get mocked timestamp"""
        return self._timestamp
    
    def advance(self, seconds: float) -> None:
        """Advance time by specified seconds"""
        from datetime import timedelta
        self._timestamp += seconds
        self._current_time += timedelta(seconds=seconds)
    
    def set_time(self, new_time: datetime) -> None:
        """Set the clock to a specific time"""
        self._current_time = new_time
        self._timestamp = new_time.timestamp()