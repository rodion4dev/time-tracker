"""Настройки проекта."""
from pydantic import BaseSettings


class SettingsStorage(BaseSettings):
    """Хранилище настроек из переменных окружения и .env файла."""


storage = SettingsStorage()
