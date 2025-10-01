"""Application entry point for the Pomodoro timer web app."""
from __future__ import annotations

import os

from factories import create_app, socketio


def main() -> None:
	"""Run the development server."""
	config_name = os.environ.get("POMODORO_CONFIG")
	app = create_app(config_name)
	socketio.run(app, host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))


if __name__ == "__main__":
	main()
