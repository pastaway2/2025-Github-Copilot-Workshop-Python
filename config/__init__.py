"""Configuration package for the Pomodoro application."""
from typing import Type

from .base import BaseConfig
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

ConfigType = Type[BaseConfig]

CONFIG_MAP = {
	"base": BaseConfig,
	"development": DevelopmentConfig,
	"testing": TestingConfig,
	"production": ProductionConfig,
}


def get_config(config_name: str | None) -> ConfigType:
	"""Return configuration class by name, defaulting to development."""
	if not config_name:
		return DevelopmentConfig
	key = config_name.lower()
	if key not in CONFIG_MAP:
		raise KeyError(f"Unknown configuration '{config_name}'.")
	return CONFIG_MAP[key]