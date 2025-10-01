"""
Pure business logic for Pomodoro Timer
"""
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from interfaces.clock import ClockInterface
from interfaces.events import EventEmitterInterface, TimerEventArgs


class TimerState(Enum):
    """Timer states"""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


class SessionType(Enum):
    """Session types"""
    WORK = "work"
    SHORT_BREAK = "short_break"
    LONG_BREAK = "long_break"


@dataclass
class TimerConfig:
    """Timer configuration"""
    work_duration: int = 25 * 60      # 25 minutes in seconds
    short_break_duration: int = 5 * 60  # 5 minutes in seconds
    long_break_duration: int = 15 * 60  # 15 minutes in seconds
    sessions_until_long_break: int = 4


class PomodoroTimer:
    """Pure business logic for Pomodoro timer - framework agnostic"""
    
    def __init__(self, 
                 config: TimerConfig,
                 clock: ClockInterface,
                 event_emitter: Optional[EventEmitterInterface] = None):
        self._config = config
        self._clock = clock
        self._event_emitter = event_emitter
        self._state = TimerState.IDLE
        self._session_type = SessionType.WORK
        self._start_time: Optional[float] = None
        self._pause_time: Optional[float] = None
        self._paused_duration: float = 0.0
    
    @property
    def state(self) -> TimerState:
        """Get current timer state"""
        return self._state
    
    @property
    def session_type(self) -> SessionType:
        """Get current session type"""
        return self._session_type
    
    def get_session_duration(self) -> int:
        """Get total duration for current session type in seconds"""
        if self._session_type == SessionType.WORK:
            return self._config.work_duration
        elif self._session_type == SessionType.SHORT_BREAK:
            return self._config.short_break_duration
        else:  # LONG_BREAK
            return self._config.long_break_duration
    
    def get_remaining_seconds(self) -> int:
        """Get remaining time in seconds"""
        if self._state == TimerState.IDLE:
            return self.get_session_duration()
        
        if self._state == TimerState.COMPLETED:
            return 0
        
        if self._start_time is None:
            return self.get_session_duration()
        
        current_time = self._clock.timestamp()
        
        if self._state == TimerState.PAUSED and self._pause_time is not None:
            elapsed = (self._pause_time - self._start_time) - self._paused_duration
        else:
            elapsed = (current_time - self._start_time) - self._paused_duration
        
        remaining = self.get_session_duration() - elapsed
        
        # Check if timer should be completed
        if remaining <= 0:
            if self._state == TimerState.RUNNING:
                self._complete_session()
            return 0
        
        return max(0, int(remaining))
    
    def start(self) -> bool:
        """Start the timer - returns True if successful"""
        if self._state == TimerState.COMPLETED:
            return False
        
        current_time = self._clock.timestamp()
        
        if self._state == TimerState.IDLE:
            self._start_time = current_time
            self._paused_duration = 0.0
        elif self._state == TimerState.PAUSED:
            if self._pause_time is not None:
                self._paused_duration += current_time - self._pause_time
            self._pause_time = None
        
        self._state = TimerState.RUNNING
        self._emit_event('timer_started')
        return True
    
    def pause(self) -> bool:
        """Pause the timer"""
        if self._state != TimerState.RUNNING:
            return False
        
        self._state = TimerState.PAUSED
        self._pause_time = self._clock.timestamp()
        self._emit_event('timer_paused')
        return True
    
    def reset(self) -> None:
        """Reset the timer to initial state"""
        self._state = TimerState.IDLE
        self._start_time = None
        self._pause_time = None
        self._paused_duration = 0.0
        self._emit_event('timer_reset')
    
    def set_session_type(self, session_type: SessionType) -> None:
        """Set the session type (only allowed when IDLE)"""
        if self._state == TimerState.IDLE:
            self._session_type = session_type
            self._emit_event('session_type_changed')
    
    def _complete_session(self) -> None:
        """Mark session as completed"""
        self._state = TimerState.COMPLETED
        self._emit_event('timer_completed')
    
    def _emit_event(self, event_name: str) -> None:
        """Emit timer event with current state"""
        if self._event_emitter:
            args = TimerEventArgs(
                remaining_seconds=self.get_remaining_seconds(),
                total_seconds=self.get_session_duration(),
                session_type=self._session_type.value
            )
            self._event_emitter.emit(event_name, self, args)