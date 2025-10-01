# Pomodoro Timer Web Application Architecture

## Project Overview

This document outlines the architecture for a Pomodoro timer web application built with Flask and modern web technologies. The application features a Japanese-language interface with a circular progress indicator, real-time updates, and session tracking capabilities.

## UI Design Requirements

Based on the provided mockup, the application includes:
- **Title**: "ポモドーロタイマー" (Pomodoro Timer)
- **Circular Progress Indicator**: Animated countdown display showing "25:00"
- **Status Display**: "作業中" (Working) indicator
- **Control Buttons**: "開始" (Start) and "リセット" (Reset)
- **Progress Tracking**: "今日の進捗" (Today's Progress) section showing completed sessions (4) and total focus time (1時間40分)
- **Visual Design**: Purple gradient background with clean, modern card-based layout

## Technology Stack

### Backend
- **Flask**: Web framework with application factory pattern
- **Flask-SocketIO**: Real-time WebSocket communication
- **SQLite**: Session persistence (easily upgradeable to PostgreSQL)
- **pytest**: Comprehensive testing framework

### Frontend
- **HTML5**: Semantic markup with Japanese language support
- **CSS3**: Modern styling with CSS Grid/Flexbox, animations, and custom properties
- **JavaScript (ES6+)**: Client-side timer logic and WebSocket handling
- **SVG**: Circular progress indicator implementation

### Development & Testing
- **pytest**: Unit and integration testing
- **pytest-cov**: Code coverage analysis
- **Factory Boy**: Test data generation
- **Hypothesis**: Property-based testing for edge cases

## Project Structure

```
/workspaces/2025-Github-Copilot-Workshop-Python/
├── app.py                    # Flask application factory
├── config/
│   ├── __init__.py
│   ├── base.py              # Base configuration
│   ├── development.py       # Development config
│   ├── testing.py           # Test-specific config
│   └── production.py        # Production config
├── models/
│   ├── __init__.py
│   ├── timer.py             # Pure business logic (no Flask deps)
│   ├── session.py           # Session domain models
│   └── events.py            # Event system interfaces
├── services/
│   ├── __init__.py
│   ├── timer_service.py     # Timer operations (injectable deps)
│   ├── session_service.py   # Session management
│   └── notification_service.py # Notification handling
├── repositories/
│   ├── __init__.py
│   ├── base.py              # Abstract repository interfaces
│   ├── session_repository.py # Session data access
│   └── memory_repository.py  # In-memory implementation for tests
├── interfaces/
│   ├── __init__.py
│   ├── clock.py             # Time abstraction for testing
│   ├── storage.py           # Storage abstraction
│   └── events.py            # Event emitter interfaces
├── factories/
│   ├── __init__.py
│   └── app_factory.py       # Dependency injection container
├── routes/
│   ├── __init__.py
│   ├── main.py              # Main web routes
│   ├── api.py               # REST API endpoints
│   └── websocket.py         # WebSocket handlers
├── templates/
│   ├── base.html            # Base template
│   └── index.html           # Main timer interface
├── static/
│   ├── css/
│   │   ├── style.css        # Main stylesheet
│   │   └── components.css   # Component-specific styles
│   ├── js/
│   │   ├── timer.js         # Timer functionality
│   │   ├── websocket.js     # WebSocket client
│   │   ├── ui.js            # UI interactions
│   │   └── components/
│   │       └── circular-progress.js # Circular progress component
│   └── images/
│       └── pomodoro.png     # Application assets
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest fixtures and configuration
│   ├── unit/
│   │   ├── test_timer.py
│   │   ├── test_session.py
│   │   ├── test_services.py
│   │   └── test_repositories.py
│   ├── integration/
│   │   ├── test_api.py
│   │   ├── test_websocket.py
│   │   └── test_full_flow.py
│   ├── property/
│   │   └── test_timer_properties.py # Property-based tests
│   ├── performance/
│   │   └── test_timer_performance.py # Performance tests
│   ├── fixtures/
│   │   ├── session_data.py
│   │   └── timer_data.py
│   └── helpers/
│       ├── test_client.py
│       └── mock_factories.py
└── requirements/
    ├── base.txt             # Core dependencies
    ├── development.txt      # Dev dependencies
    └── testing.txt          # Test dependencies
```

## Architecture Principles

### 1. Separation of Concerns
- **Models**: Pure business logic with no framework dependencies
- **Services**: Application logic with dependency injection
- **Repositories**: Data access abstraction
- **Routes**: HTTP/WebSocket handling
- **Templates**: Presentation layer

### 2. Dependency Injection
All external dependencies are injected through interfaces, enabling:
- Easy unit testing with mocks
- Configurable implementations (in-memory vs. database)
- Loose coupling between components

### 3. Event-Driven Architecture
Timer events are emitted for:
- Real-time UI updates via WebSockets
- Session completion handling
- Statistics updates
- Decoupled component communication

### 4. Testability
- **Pure Functions**: Business logic isolated from side effects
- **Mock Interfaces**: Time, storage, and events can be mocked
- **Repository Pattern**: Data access easily stubbed
- **Configuration Isolation**: Test-specific settings

## Core Components

### Timer Business Logic

```python
# models/timer.py
class PomodoroTimer:
    """Pure business logic - framework agnostic"""
    
    def __init__(self, config: TimerConfig, clock: ClockInterface, 
                 event_emitter: Optional[EventEmitterInterface] = None):
        self._config = config
        self._clock = clock
        self._event_emitter = event_emitter
        self._state = TimerState.IDLE
    
    def start(self) -> bool:
        """Start the timer - returns True if successful"""
    
    def pause(self) -> bool:
        """Pause the timer"""
    
    def reset(self) -> None:
        """Reset the timer to initial state"""
    
    def get_remaining_seconds(self) -> int:
        """Get remaining time in seconds"""
```

### Service Layer

```python
# services/timer_service.py
class TimerService:
    """Application service with injected dependencies"""
    
    def __init__(self, session_repository: SessionRepositoryInterface,
                 clock: ClockInterface, event_emitter: EventEmitterInterface):
        self._repository = session_repository
        self._clock = clock
        self._event_emitter = event_emitter
    
    def create_session(self, session_type: str = "work") -> str:
        """Create a new timer session"""
    
    def start_timer(self) -> bool:
        """Start the current timer"""
    
    def complete_session(self) -> PomodoroSession:
        """Complete and save the current session"""
```

### Repository Pattern

```python
# repositories/base.py
class SessionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, session: PomodoroSession) -> PomodoroSession: ...
    
    @abstractmethod
    def get_by_date(self, date: date) -> List[PomodoroSession]: ...
    
    @abstractmethod
    def get_completed_sessions_count(self, date: date) -> int: ...
```

## Frontend Architecture

### Circular Progress Component

```javascript
// static/js/components/circular-progress.js
class CircularProgress {
    constructor(element, radius = 90) {
        this.element = element;
        this.circumference = 2 * Math.PI * radius;
        this.setupSVG();
    }
    
    setProgress(percentage) {
        // Animate circular progress indicator
    }
}
```

### Timer Controller

```javascript
// static/js/timer.js
class PomodoroTimer {
    constructor() {
        this.websocket = new WebSocketClient();
        this.ui = new UIManager(this);
        this.progressRing = new CircularProgress(
            document.getElementById('progress-ring')
        );
    }
    
    start() {
        // Start timer with WebSocket sync
    }
    
    updateDisplay(timeRemaining) {
        // Update UI with current time
        this.progressRing.setProgress(this.calculateProgress(timeRemaining));
    }
}
```

## API Design

### REST Endpoints

- `POST /api/timer/start` - Start a new timer session
- `GET /api/timer/status` - Get current timer state
- `POST /api/timer/pause` - Pause current session
- `POST /api/timer/reset` - Reset current session
- `GET /api/sessions/today` - Get today's session statistics
- `GET /api/sessions/history` - Get session history

### WebSocket Events

#### Client → Server
- `start_timer` - Start timer request
- `pause_timer` - Pause timer request
- `reset_timer` - Reset timer request

#### Server → Client
- `timer_started` - Timer started confirmation
- `timer_update` - Real-time timer updates
- `timer_paused` - Timer paused notification
- `timer_completed` - Session completion
- `session_stats_updated` - Updated daily statistics

## CSS Architecture

### Design System

```css
:root {
    /* Color Palette */
    --primary-purple: #6366f1;
    --light-purple: #a5b4fc;
    --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --card-background: #ffffff;
    --text-dark: #374151;
    --text-light: #6b7280;
    
    /* Typography */
    --font-family: 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif;
    --font-size-xl: 2.5rem;
    --font-size-lg: 1.5rem;
    --font-size-base: 1rem;
    
    /* Spacing */
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 1.5rem;
    --spacing-lg: 2rem;
    --spacing-xl: 3rem;
    
    /* Animation */
    --transition-base: 0.3s ease;
    --transition-slow: 0.6s ease;
}
```

### Component Styling

```css
.timer-card {
    background: var(--card-background);
    border-radius: 24px;
    padding: var(--spacing-xl) var(--spacing-lg);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    max-width: 400px;
}

.circular-timer {
    position: relative;
    width: 200px;
    height: 200px;
    margin: 0 auto var(--spacing-xl);
}

.progress-ring-circle {
    stroke: var(--primary-purple);
    stroke-dasharray: 628; /* 2 * π * 100 */
    transition: stroke-dashoffset var(--transition-base);
}
```

## Testing Strategy

### Unit Tests
- **Pure Business Logic**: Timer operations, state management
- **Service Layer**: Application logic with mocked dependencies
- **Repository Layer**: Data access with in-memory implementations

### Integration Tests
- **API Endpoints**: HTTP request/response testing
- **WebSocket Events**: Real-time communication testing
- **Full Flow**: End-to-end user scenarios

### Property-Based Tests
- **Timer Accuracy**: Verify remaining time calculations
- **Edge Cases**: Pause/resume scenarios, boundary conditions

### Performance Tests
- **Real-time Updates**: Ensure UI responsiveness
- **Concurrent Access**: Thread safety verification

## Implementation Phases

### Phase 1: Core Functionality (Week 1)
- Basic Flask application with timer business logic
- Simple HTML interface matching mockup layout
- Start/Reset button functionality
- In-memory session storage

### Phase 2: UI Enhancement (Week 2)
- Implement purple gradient design
- Add animated circular progress indicator
- Japanese text styling and typography
- Responsive mobile design

### Phase 3: Real-time Features (Week 3)
- WebSocket integration for live updates
- Session statistics implementation
- Cross-tab synchronization
- Basic unit test coverage

### Phase 4: Polish & Advanced Features (Week 4)
- Sound notifications on completion
- Browser notifications (with permission)
- Session persistence with SQLite
- Comprehensive test suite
- Performance optimization

## Configuration Management

### Development Configuration
```python
# config/development.py
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TIMER_WORK_DURATION = 25 * 60    # 25 minutes
    TIMER_SHORT_BREAK = 5 * 60       # 5 minutes
    TIMER_LONG_BREAK = 15 * 60       # 15 minutes
    DATABASE_URL = "sqlite:///pomodoro_dev.db"
```

### Testing Configuration
```python
# config/testing.py
class TestConfig(BaseConfig):
    TESTING = True
    TIMER_WORK_DURATION = 5          # 5 seconds for fast tests
    TIMER_SHORT_BREAK = 2            # 2 seconds
    DATABASE_URL = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
```

## Security Considerations

- **CSRF Protection**: Enabled for all state-changing operations
- **Input Validation**: All user inputs validated and sanitized
- **Session Management**: Secure session handling
- **WebSocket Security**: Origin validation and rate limiting

## Performance Requirements

- **Timer Accuracy**: ±1 second precision for 25-minute sessions
- **UI Responsiveness**: Updates within 100ms of state changes
- **Memory Usage**: Minimal background resource consumption
- **Network Efficiency**: WebSocket events < 1KB payload

## Monitoring & Analytics

- **Session Completion Rate**: Track user engagement
- **Average Session Duration**: Monitor actual vs. intended usage
- **Error Tracking**: Client-side and server-side error logging
- **Performance Metrics**: Response times and resource usage

## Deployment Strategy

### Development
- Local SQLite database
- Flask development server
- Hot reload for static assets

### Production
- PostgreSQL database
- Gunicorn + Nginx
- WebSocket support with Redis
- SSL/TLS encryption

## Accessibility Features

- **Keyboard Navigation**: Full keyboard support for all controls
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **High Contrast Mode**: Alternative color schemes
- **Reduced Motion**: Respect user motion preferences
- **Focus Management**: Clear focus indicators

## Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Progressive Enhancement**: Core functionality without JavaScript
- **WebSocket Fallback**: Polling mechanism for older browsers

## Conclusion

This architecture provides a solid foundation for a production-ready Pomodoro timer application that is:
- **Maintainable**: Clean separation of concerns and dependency injection
- **Testable**: Comprehensive testing strategy with high coverage
- **Scalable**: Modular design allowing for future enhancements
- **User-Friendly**: Modern UI matching the provided mockup design
- **Performant**: Real-time updates with minimal resource usage

The implementation follows modern web development best practices while maintaining simplicity and focusing on the core user experience of an effective Pomodoro timer.