# Pomodoro Timer Application - Function Implementation List

This document outlines all the necessary functions that need to be implemented for the Pomodoro timer web application, organized by module and responsibility.

## 1. Core Timer Business Logic (`models/timer.py`)

### `PomodoroTimer` Class
- `__init__(self, config: TimerConfig, clock: ClockInterface, event_emitter: Optional[EventEmitterInterface] = None)` - Initialize timer with dependencies
- `start(self) -> bool` - Start the timer, return success boolean
- `pause(self) -> bool` - Pause the timer, return success boolean  
- `resume(self) -> bool` - Resume paused timer
- `reset(self) -> None` - Reset timer to initial state
- `get_remaining_seconds(self) -> int` - Get current remaining time
- `get_elapsed_seconds(self) -> int` - Get elapsed time since start
- `get_state(self) -> TimerState` - Get current timer state (IDLE, RUNNING, PAUSED, COMPLETED)
- `is_running(self) -> bool` - Check if timer is currently running
- `is_paused(self) -> bool` - Check if timer is paused
- `update(self) -> None` - Update timer state (called periodically)
- `_emit_event(self, event_name: str, data: dict = None)` - Internal event emission helper

### `TimerConfig` Class
- `__init__(self, work_duration: int = 1500, short_break: int = 300, long_break: int = 900)` - Configuration settings (25min, 5min, 15min)
- `get_work_duration(self) -> int` - Get work session duration in seconds
- `get_short_break_duration(self) -> int` - Get short break duration in seconds
- `get_long_break_duration(self) -> int` - Get long break duration in seconds
- `to_dict(self) -> dict` - Convert configuration to dictionary

### `TimerState` Enum
- `IDLE` - Timer not started
- `RUNNING` - Timer actively counting down
- `PAUSED` - Timer paused
- `COMPLETED` - Timer completed

## 2. Session Management (`models/session.py`)

### `PomodoroSession` Class
- `__init__(self, session_type: SessionType, start_time: datetime, duration: int)` - Create session
- `complete(self, end_time: datetime) -> None` - Mark session as completed
- `get_duration(self) -> int` - Get actual session duration in seconds
- `get_actual_duration(self) -> int` - Get time between start and completion
- `is_completed(self) -> bool` - Check completion status
- `to_dict(self) -> dict` - Convert to dictionary for serialization
- `from_dict(cls, data: dict) -> 'PomodoroSession'` - Create from dictionary (class method)

### `SessionType` Enum
- `WORK` - Work session (25 minutes)
- `SHORT_BREAK` - Short break (5 minutes)
- `LONG_BREAK` - Long break (15 minutes)

### `SessionStats` Class
- `__init__(self, date: date, completed_sessions: int = 0, total_focus_time: int = 0)` - Daily statistics
- `add_session(self, session: PomodoroSession) -> None` - Add completed session to stats
- `get_completed_work_sessions(self) -> int` - Get count of completed work sessions
- `get_total_focus_time_minutes(self) -> int` - Get total focus time in minutes
- `to_dict(self) -> dict` - Convert to dictionary

## 3. Event System (`models/events.py`)

### `TimerEvent` Class
- `__init__(self, event_type: str, data: dict = None, timestamp: datetime = None)` - Create event
- `to_dict(self) -> dict` - Convert event to dictionary

### Event Types Constants
- `TIMER_STARTED = "timer_started"`
- `TIMER_PAUSED = "timer_paused"`
- `TIMER_RESUMED = "timer_resumed"`
- `TIMER_RESET = "timer_reset"`
- `TIMER_COMPLETED = "timer_completed"`
- `TIMER_TICK = "timer_tick"`
- `SESSION_STATS_UPDATED = "session_stats_updated"`

## 4. Service Layer

### `TimerService` Class (`services/timer_service.py`)
- `__init__(self, session_repository: SessionRepositoryInterface, clock: ClockInterface, event_emitter: EventEmitterInterface)` - Initialize with dependencies
- `create_session(self, session_type: SessionType = SessionType.WORK) -> str` - Create new timer session, return session ID
- `start_timer(self) -> bool` - Start current session
- `pause_timer(self) -> bool` - Pause current session
- `resume_timer(self) -> bool` - Resume paused session
- `reset_timer(self) -> None` - Reset current session
- `complete_session(self) -> PomodoroSession` - Complete and save session
- `get_current_session(self) -> Optional[PomodoroSession]` - Get current session info
- `get_timer_status(self) -> dict` - Get comprehensive timer status
- `update_timer(self) -> None` - Update timer state (for background processing)

### `SessionService` Class (`services/session_service.py`)
- `__init__(self, session_repository: SessionRepositoryInterface)` - Initialize with repository
- `save_session(self, session: PomodoroSession) -> PomodoroSession` - Save completed session
- `get_sessions_by_date(self, date: date) -> List[PomodoroSession]` - Get sessions for specific date
- `get_today_sessions(self) -> List[PomodoroSession]` - Get today's sessions
- `get_completed_sessions_count(self, date: date) -> int` - Count completed sessions
- `get_total_focus_time(self, date: date) -> int` - Calculate total focus time in seconds
- `get_session_statistics(self, date: date) -> SessionStats` - Get comprehensive stats
- `get_weekly_statistics(self, week_start: date) -> List[SessionStats]` - Get weekly stats

### `NotificationService` Class (`services/notification_service.py`)
- `__init__(self, event_emitter: EventEmitterInterface)` - Initialize with event system
- `send_session_complete_notification(self, session: PomodoroSession) -> None` - Send completion notification
- `send_break_reminder(self, session_type: SessionType) -> None` - Send break reminder
- `play_completion_sound(self) -> None` - Play audio notification
- `show_browser_notification(self, title: str, message: str) -> None` - Show browser notification

## 5. Repository Layer

### `SessionRepositoryInterface` Class (`repositories/base.py`)
- `save(self, session: PomodoroSession) -> PomodoroSession` - Save session (abstract)
- `get_by_id(self, session_id: str) -> Optional[PomodoroSession]` - Get session by ID (abstract)
- `get_by_date(self, date: date) -> List[PomodoroSession]` - Get sessions by date (abstract)
- `get_completed_sessions_count(self, date: date) -> int` - Count sessions (abstract)
- `get_all(self) -> List[PomodoroSession]` - Get all sessions (abstract)
- `delete(self, session_id: str) -> bool` - Delete session (abstract)

### `SqliteSessionRepository` Class (`repositories/session_repository.py`)
- `__init__(self, db_path: str)` - Initialize database connection
- `save(self, session: PomodoroSession) -> PomodoroSession` - Save session to SQLite
- `get_by_id(self, session_id: str) -> Optional[PomodoroSession]` - Query session by ID
- `get_by_date(self, date: date) -> List[PomodoroSession]` - Query sessions by date
- `get_completed_sessions_count(self, date: date) -> int` - Count completed sessions
- `get_all(self) -> List[PomodoroSession]` - Get all sessions
- `delete(self, session_id: str) -> bool` - Delete session
- `create_tables(self) -> None` - Create database schema
- `close(self) -> None` - Close database connection
- `_row_to_session(self, row: sqlite3.Row) -> PomodoroSession` - Convert DB row to session object

### `MemorySessionRepository` Class (`repositories/memory_repository.py`)
- `__init__(self)` - Initialize in-memory storage
- `save(self, session: PomodoroSession) -> PomodoroSession` - Save to memory
- `get_by_id(self, session_id: str) -> Optional[PomodoroSession]` - Get by ID from memory
- `get_by_date(self, date: date) -> List[PomodoroSession]` - Filter sessions by date
- `get_completed_sessions_count(self, date: date) -> int` - Count sessions
- `get_all(self) -> List[PomodoroSession]` - Get all sessions
- `delete(self, session_id: str) -> bool` - Delete from memory
- `clear(self) -> None` - Clear all data (for testing)

## 6. Interface Abstractions

### `ClockInterface` Class (`interfaces/clock.py`)
- `now(self) -> datetime` - Get current time (abstract)
- `sleep(self, seconds: float) -> None` - Sleep for specified time (abstract)

### `SystemClock` Class (`interfaces/clock.py`)
- `now(self) -> datetime` - Return actual system time
- `sleep(self, seconds: float) -> None` - Actual sleep implementation

### `MockClock` Class (`interfaces/clock.py`)
- `__init__(self, initial_time: datetime = None)` - Set mock time
- `now(self) -> datetime` - Return mock time
- `advance(self, seconds: int) -> None` - Advance mock time
- `sleep(self, seconds: float) -> None` - Mock sleep (no actual delay)
- `set_time(self, time: datetime) -> None` - Set specific mock time

### `EventEmitterInterface` Class (`interfaces/events.py`)
- `emit(self, event_name: str, data: dict = None) -> None` - Emit event (abstract)
- `on(self, event_name: str, callback: Callable) -> None` - Register event listener (abstract)
- `off(self, event_name: str, callback: Callable = None) -> None` - Remove event listener (abstract)

### `FlaskSocketIOEventEmitter` Class (`interfaces/events.py`)
- `__init__(self, socketio)` - Initialize with Flask-SocketIO instance
- `emit(self, event_name: str, data: dict = None) -> None` - Emit via WebSocket
- `on(self, event_name: str, callback: Callable) -> None` - Register WebSocket listener
- `off(self, event_name: str, callback: Callable = None) -> None` - Remove WebSocket listener

## 7. Flask Application (`app.py`)

### Application Factory Functions
- `create_app(config_name: str = 'development') -> Flask` - Create Flask application
- `configure_app(app: Flask, config: object) -> None` - Apply configuration
- `register_blueprints(app: Flask) -> None` - Register route blueprints
- `configure_socketio(app: Flask) -> SocketIO` - Setup WebSocket support
- `configure_database(app: Flask) -> None` - Setup database connections
- `setup_dependency_injection(app: Flask) -> None` - Configure DI container

### Dependency Injection (`factories/app_factory.py`)
- `create_timer_service(app: Flask) -> TimerService` - Create timer service with dependencies
- `create_session_service(app: Flask) -> SessionService` - Create session service
- `create_session_repository(app: Flask) -> SessionRepositoryInterface` - Create repository
- `create_clock() -> ClockInterface` - Create clock implementation
- `create_event_emitter(socketio: SocketIO) -> EventEmitterInterface` - Create event emitter

## 8. Web Routes

### Main Routes (`routes/main.py`)
- `index() -> str` - Render main timer page (GET /)
- `about() -> str` - About page (GET /about) [optional]

### API Routes (`routes/api.py`)
- `start_timer() -> Response` - Start timer (POST /api/timer/start)
- `pause_timer() -> Response` - Pause timer (POST /api/timer/pause)
- `resume_timer() -> Response` - Resume timer (POST /api/timer/resume)
- `reset_timer() -> Response` - Reset timer (POST /api/timer/reset)
- `get_timer_status() -> Response` - Get timer status (GET /api/timer/status)
- `get_today_sessions() -> Response` - Get today's sessions (GET /api/sessions/today)
- `get_session_history() -> Response` - Get session history (GET /api/sessions/history)
- `create_session(session_type: str) -> Response` - Create new session (POST /api/sessions)

### WebSocket Handlers (`routes/websocket.py`)
- `handle_connect(auth: dict) -> None` - Client connection handler
- `handle_disconnect() -> None` - Client disconnection handler
- `handle_start_timer(data: dict) -> None` - Start timer WebSocket event
- `handle_pause_timer(data: dict) -> None` - Pause timer WebSocket event
- `handle_resume_timer(data: dict) -> None` - Resume timer WebSocket event
- `handle_reset_timer(data: dict) -> None` - Reset timer WebSocket event
- `emit_timer_update(timer_data: dict) -> None` - Send timer updates to clients
- `emit_session_complete(session_data: dict) -> None` - Send completion notifications
- `background_timer_task() -> None` - Background task for timer updates

## 9. Frontend JavaScript

### Timer Controller (`static/js/timer.js`)
- `class PomodoroTimer` - Main timer controller class
  - `constructor()` - Initialize timer with WebSocket and UI components
  - `start() -> Promise<void>` - Start timer functionality
  - `pause() -> Promise<void>` - Pause timer
  - `resume() -> Promise<void>` - Resume timer
  - `reset() -> Promise<void>` - Reset timer
  - `updateDisplay(timeRemaining: number) -> void` - Update UI display
  - `calculateProgress(timeRemaining: number) -> number` - Calculate progress percentage
  - `formatTime(seconds: number) -> string` - Format time for display (MM:SS)
  - `handleTimerComplete(sessionData: object) -> void` - Handle completion events
  - `loadTodayStats() -> Promise<void>` - Load today's statistics
  - `syncWithServer() -> Promise<void>` - Synchronize with server state

### WebSocket Client (`static/js/websocket.js`)
- `class WebSocketClient` - WebSocket communication handler
  - `constructor(url: string)` - Initialize WebSocket connection
  - `connect() -> Promise<void>` - Establish WebSocket connection
  - `disconnect() -> void` - Close WebSocket connection
  - `emit(event: string, data: object) -> void` - Send events to server
  - `on(event: string, callback: function) -> void` - Register event listeners
  - `off(event: string, callback: function) -> void` - Remove event listeners
  - `handleConnectionLost() -> void` - Handle connection errors
  - `handleReconnect() -> void` - Handle reconnection logic
  - `isConnected() -> boolean` - Check connection status

### UI Manager (`static/js/ui.js`)
- `class UIManager` - UI state management
  - `constructor(timerInstance: PomodoroTimer)` - Initialize with timer reference
  - `updateTimerDisplay(time: string) -> void` - Update timer text display
  - `updateProgressBar(percentage: number) -> void` - Update progress indicator
  - `updateSessionStats(stats: object) -> void` - Update statistics display
  - `showNotification(message: string, type: string) -> void` - Show user notifications
  - `toggleButtons(state: string) -> void` - Enable/disable control buttons
  - `showSessionComplete(sessionType: string) -> void` - Show completion message
  - `updateStatusText(status: string) -> void` - Update status indicator
  - `handleError(error: string) -> void` - Handle and display errors

### Circular Progress Component (`static/js/components/circular-progress.js`)
- `class CircularProgress` - Animated progress ring component
  - `constructor(element: HTMLElement, radius: number = 90)` - Initialize SVG progress ring
  - `setupSVG() -> void` - Initialize SVG elements and attributes
  - `setProgress(percentage: number) -> void` - Animate progress ring to percentage
  - `reset() -> void` - Reset progress to zero
  - `animate(from: number, to: number, duration: number) -> Promise<void>` - Smooth animations
  - `setColor(color: string) -> void` - Change progress ring color
  - `resize(newRadius: number) -> void` - Resize the progress ring

## 10. Configuration System

### Base Configuration (`config/base.py`)
- `class BaseConfig` - Base configuration class
  - `TIMER_WORK_DURATION = 25 * 60` - Work session duration (25 minutes)
  - `TIMER_SHORT_BREAK = 5 * 60` - Short break duration (5 minutes)
  - `TIMER_LONG_BREAK = 15 * 60` - Long break duration (15 minutes)
  - `SECRET_KEY` - Flask secret key
  - `get_database_url(self) -> str` - Database connection string
  - `get_timer_config(self) -> dict` - Timer configuration dictionary

### Development Configuration (`config/development.py`)
- `class DevelopmentConfig(BaseConfig)` - Development settings
  - `DEBUG = True` - Enable debug mode
  - `DATABASE_URL = "sqlite:///pomodoro_dev.db"` - Development database

### Testing Configuration (`config/testing.py`)
- `class TestConfig(BaseConfig)` - Test configuration
  - `TESTING = True` - Enable testing mode
  - `TIMER_WORK_DURATION = 5` - Fast timer for testing (5 seconds)
  - `TIMER_SHORT_BREAK = 2` - Fast break (2 seconds)
  - `DATABASE_URL = "sqlite:///:memory:"` - In-memory database
  - `WTF_CSRF_ENABLED = False` - Disable CSRF for testing

### Production Configuration (`config/production.py`)
- `class ProductionConfig(BaseConfig)` - Production settings
  - `DEBUG = False` - Disable debug mode
  - `DATABASE_URL` - Production database URL from environment

## 11. Testing Functions

### Unit Tests (`tests/unit/`)

#### Timer Tests (`test_timer.py`)
- `test_timer_initialization()` - Test timer creation
- `test_timer_start()` - Test timer start functionality
- `test_timer_pause_resume()` - Test pause/resume cycle
- `test_timer_reset()` - Test reset functionality
- `test_timer_completion()` - Test timer completion
- `test_timer_state_transitions()` - Test state changes
- `test_timer_accuracy()` - Test timing accuracy

#### Session Tests (`test_session.py`)
- `test_session_creation()` - Test session management
- `test_session_completion()` - Test session completion
- `test_session_serialization()` - Test to_dict/from_dict
- `test_session_stats()` - Test statistics calculation

#### Service Tests (`test_services.py`)
- `test_timer_service_operations()` - Test timer service
- `test_session_service_crud()` - Test session CRUD operations
- `test_notification_service()` - Test notification handling

#### Repository Tests (`test_repositories.py`)
- `test_memory_repository()` - Test in-memory implementation
- `test_sqlite_repository()` - Test SQLite implementation
- `test_repository_data_persistence()` - Test data persistence

### Integration Tests (`tests/integration/`)

#### API Tests (`test_api.py`)
- `test_timer_api_endpoints()` - Test REST API endpoints
- `test_session_api_endpoints()` - Test session API
- `test_api_error_handling()` - Test error responses
- `test_api_authentication()` - Test API security

#### WebSocket Tests (`test_websocket.py`)
- `test_websocket_connection()` - Test WebSocket connectivity
- `test_real_time_updates()` - Test real-time communication
- `test_websocket_error_handling()` - Test WebSocket errors

#### Full Flow Tests (`test_full_flow.py`)
- `test_complete_timer_session()` - End-to-end session test
- `test_multi_session_workflow()` - Test multiple sessions
- `test_cross_tab_synchronization()` - Test multi-tab sync

### Property-Based Tests (`tests/property/`)
- `test_timer_properties()` - Property-based timer tests
- `test_session_invariants()` - Test session data invariants
- `test_time_calculations()` - Test time calculation accuracy

### Performance Tests (`tests/performance/`)
- `test_timer_performance()` - Test timer responsiveness
- `test_database_performance()` - Test database operations
- `test_websocket_performance()` - Test real-time update performance

### Test Fixtures and Helpers (`tests/`)
- `conftest.py` - pytest configuration and fixtures
- `fixtures/session_data.py` - Session test data factories
- `fixtures/timer_data.py` - Timer test data
- `helpers/test_client.py` - Test client utilities
- `helpers/mock_factories.py` - Mock object factories

## 12. Utility Functions

### Time Utilities (`utils/time_utils.py`)
- `format_time_mmss(seconds: int) -> str` - Format time as MM:SS
- `format_time_hhmm(minutes: int) -> str` - Format time as HH:MM (for Japanese display)
- `parse_duration(duration_string: str) -> int` - Parse duration strings to seconds
- `seconds_to_minutes(seconds: int) -> int` - Convert seconds to minutes
- `get_japanese_time_display(minutes: int) -> str` - Format for Japanese UI (e.g., "1時間40分")

### Database Utilities (`utils/db_utils.py`)
- `init_database(db_path: str) -> None` - Initialize database schema
- `migrate_database(db_path: str) -> None` - Handle schema migrations
- `backup_database(db_path: str, backup_path: str) -> None` - Create data backups
- `validate_database_schema(db_path: str) -> bool` - Validate schema integrity

### Validation Utilities (`utils/validation.py`)
- `validate_session_type(session_type: str) -> bool` - Validate session type input
- `validate_duration(duration: int) -> bool` - Validate duration values
- `sanitize_input(input_string: str) -> str` - Sanitize user input
- `validate_date_format(date_string: str) -> bool` - Validate date strings

## 13. Background Tasks (`tasks/`)

### Timer Background Process (`tasks/timer_task.py`)
- `TimerBackgroundTask` class
  - `__init__(self, timer_service: TimerService, socketio: SocketIO)` - Initialize background task
  - `start() -> None` - Start background timer updates
  - `stop() -> None` - Stop background processing
  - `update_loop() -> None` - Main update loop
  - `emit_updates() -> None` - Emit timer updates to connected clients

### Session Cleanup (`tasks/cleanup_task.py`)
- `cleanup_old_sessions(repository: SessionRepositoryInterface, days: int = 30) -> int` - Clean old sessions
- `optimize_database(db_path: str) -> None` - Optimize database performance
- `generate_daily_report(date: date, session_service: SessionService) -> dict` - Generate reports

## Implementation Priority

### Phase 1: Core Functionality
1. Timer business logic (`models/timer.py`, `models/session.py`)
2. Basic Flask app (`app.py`) 
3. Simple UI with start/reset buttons
4. In-memory storage

### Phase 2: Persistence & API
1. Repository layer (`repositories/`)
2. Service layer (`services/`)
3. REST API endpoints (`routes/api.py`)
4. SQLite integration

### Phase 3: Real-time Features
1. WebSocket implementation (`routes/websocket.py`)
2. Frontend WebSocket client (`static/js/websocket.js`)
3. Real-time UI updates
4. Circular progress component

### Phase 4: Polish & Testing
1. Comprehensive test suite (`tests/`)
2. Error handling and validation
3. Performance optimization
4. UI/UX enhancements

This comprehensive function list provides a clear roadmap for implementing the complete Pomodoro timer application with all features specified in the architecture document.