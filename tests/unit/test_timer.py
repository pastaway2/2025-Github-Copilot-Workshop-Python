"""Unit tests for PomodoroTimer business logic."""
from __future__ import annotations

from interfaces.clock import MockClock
from interfaces.events import MockEventEmitter
from models.timer import PomodoroTimer, TimerConfig, TimerState


def test_timer_counts_down_and_completes() -> None:
    clock = MockClock()
    event_emitter = MockEventEmitter()
    config = TimerConfig(work_duration=5, short_break_duration=3, long_break_duration=6)
    timer = PomodoroTimer(config=config, clock=clock, event_emitter=event_emitter)

    assert timer.state == TimerState.IDLE
    assert timer.get_remaining_seconds() == 5

    assert timer.start() is True
    assert timer.state == TimerState.RUNNING

    clock.advance(2)
    assert timer.get_remaining_seconds() == 3

    assert timer.pause() is True
    assert timer.state == TimerState.PAUSED

    clock.advance(2)
    # Remaining time shouldn't change while paused
    assert timer.get_remaining_seconds() == 3

    assert timer.start() is True
    assert timer.state == TimerState.RUNNING

    clock.advance(3)
    assert timer.get_remaining_seconds() == 0
    assert timer.state == TimerState.COMPLETED

    completed_events = event_emitter.get_emitted_events("timer_completed")
    assert len(completed_events) == 1


def test_timer_reset_restores_initial_state() -> None:
    clock = MockClock()
    config = TimerConfig(work_duration=10)
    timer = PomodoroTimer(config=config, clock=clock)

    timer.start()
    clock.advance(4)
    assert timer.get_remaining_seconds() == 6

    timer.reset()
    assert timer.state == TimerState.IDLE
    assert timer.get_remaining_seconds() == 10