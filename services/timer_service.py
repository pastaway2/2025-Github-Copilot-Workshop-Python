"""Timer application service."""
from __future__ import annotations

from typing import Dict, Any

from interfaces.clock import ClockInterface
from interfaces.events import EventEmitterInterface, TimerEventArgs
from models.timer import PomodoroTimer, TimerConfig, TimerState, SessionType
from services.session_service import SessionService


class TimerService:
    """Coordinate timer operations and session management."""

    def __init__(
        self,
        *,
        config: TimerConfig,
        clock: ClockInterface,
        event_emitter: EventEmitterInterface,
        session_service: SessionService,
    ) -> None:
        self._clock = clock
        self._config = config
        self._event_emitter = event_emitter
        self._session_service = session_service
        self._timer = PomodoroTimer(config, clock, event_emitter)

        self._event_emitter.on("timer_completed", self._handle_timer_completed)

    def start_timer(self, session_type: str = "work") -> bool:
        """Start the timer and create a session when idle."""
        if self._timer.state == TimerState.RUNNING:
            return False

        if self._timer.state == TimerState.COMPLETED:
            self._timer.reset()

        if session_type != self._timer.session_type.value:
            try:
                self._timer.set_session_type(SessionType(session_type))
            except ValueError as exc:  # Unknown session type
                raise ValueError(f"Unsupported session type '{session_type}'") from exc

        self._session_service.start_session(self._timer.session_type.value)
        return self._timer.start()

    def reset_timer(self) -> None:
        """Reset the timer and discard the active session."""
        self._timer.reset()
        self._session_service.discard_current_session()

    def get_status(self) -> Dict[str, Any]:
        """Return a serializable snapshot of the timer state."""
        remaining = self._timer.get_remaining_seconds()
        return {
            "state": self._timer.state.value,
            "session_type": self._timer.session_type.value,
            "remaining_seconds": remaining,
            "total_seconds": self._timer.get_session_duration(),
        }

    def _handle_timer_completed(self, sender, args: TimerEventArgs) -> None:
        """Persist a completed session."""
        self._session_service.complete_current_session(args.total_seconds)

    @property
    def timer(self) -> PomodoroTimer:
        """Expose the underlying timer (testing)."""
        return self._timer
