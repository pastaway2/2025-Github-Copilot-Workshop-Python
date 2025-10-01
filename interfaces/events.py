"""
Event system interfaces
"""
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List
from dataclasses import dataclass


@dataclass
class EventArgs:
    """Base class for event arguments"""
    pass


@dataclass
class TimerEventArgs(EventArgs):
    """Timer-specific event arguments"""
    remaining_seconds: int
    total_seconds: int
    session_type: str


@dataclass
class SessionEventArgs(EventArgs):
    """Session-specific event arguments"""
    session_id: str
    session_type: str
    duration_seconds: int
    completed: bool


class EventEmitterInterface(ABC):
    """Abstract interface for event emission"""
    
    @abstractmethod
    def emit(self, event_name: str, *args, **kwargs) -> None:
        """Emit an event with arguments"""
        pass
    
    @abstractmethod
    def on(self, event_name: str, handler: Callable) -> None:
        """Register event handler"""
        pass
    
    @abstractmethod
    def off(self, event_name: str, handler: Callable) -> None:
        """Unregister event handler"""
        pass


class EventEmitter(EventEmitterInterface):
    """Simple event emitter implementation"""
    
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}
    
    def emit(self, event_name: str, *args, **kwargs) -> None:
        """Emit event to all registered handlers"""
        handlers = self._handlers.get(event_name, [])
        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                # Log error but don't stop other handlers
                print(f"Error in event handler for {event_name}: {e}")
    
    def on(self, event_name: str, handler: Callable) -> None:
        """Register event handler"""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)
    
    def off(self, event_name: str, handler: Callable) -> None:
        """Unregister event handler"""
        if event_name in self._handlers:
            if handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)


class MockEventEmitter(EventEmitterInterface):
    """Mock event emitter for testing"""
    
    def __init__(self):
        self.emitted_events: List[tuple] = []
        self._handlers: Dict[str, List[Callable]] = {}
    
    def emit(self, event_name: str, *args, **kwargs) -> None:
        """Record emitted event"""
        self.emitted_events.append((event_name, args, kwargs))
        
        # Still call handlers if any are registered
        handlers = self._handlers.get(event_name, [])
        for handler in handlers:
            handler(*args, **kwargs)
    
    def on(self, event_name: str, handler: Callable) -> None:
        """Register event handler"""
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        if handler not in self._handlers[event_name]:
            self._handlers[event_name].append(handler)
    
    def off(self, event_name: str, handler: Callable) -> None:
        """Unregister event handler"""
        if event_name in self._handlers:
            if handler in self._handlers[event_name]:
                self._handlers[event_name].remove(handler)
    
    def get_emitted_events(self, event_name: str = None) -> List[tuple]:
        """Get list of emitted events, optionally filtered by name"""
        if event_name is None:
            return self.emitted_events.copy()
        return [event for event in self.emitted_events if event[0] == event_name]
    
    def clear_events(self) -> None:
        """Clear recorded events"""
        self.emitted_events.clear()