"""Настройки проекта."""
from pathlib import Path

from pydantic import BaseSettings

BASE_DIRECTORY_PATH = Path(__file__).absolute().parent.parent


class DatabaseSettings(BaseSettings):
    """Настройки баз данных."""

    class Config:
        """Мета конфигурация настроек."""

        env_file = str(BASE_DIRECTORY_PATH / '.database.env')
        env_file_encoding = 'utf-8'


class ApplicationSettings(BaseSettings):
    """Прочие настройки приложения."""

    class Config:
        """Мета конфигурация настроек."""

        env_file = str(BASE_DIRECTORY_PATH / '.env')
        env_file_encoding = 'utf-8'


database_settings, application_settings = DatabaseSettings(), ApplicationSettings()
