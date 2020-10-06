"""Настройки проекта."""
from ipaddress import IPv4Address
from pathlib import Path
from typing import Tuple, Union

from pydantic import BaseSettings, PositiveInt, RedisDsn, SecretStr

BASE_DIRECTORY_PATH = Path(__file__).absolute().parent.parent


class ApplicationSettings(BaseSettings):
    """Настройки приложения."""

    log_file_path: Path = BASE_DIRECTORY_PATH / 'log.json'

    class Config:
        """Конфигурация настроек."""

        env_file = str(BASE_DIRECTORY_PATH / '.application.env')
        env_file_encoding = 'utf-8'


class DatabaseSettings(BaseSettings):
    """Настройки баз данных."""

    redis_dsn: RedisDsn = 'redis://127.0.0.1:6379/0'
    redis_connections_count: Tuple[PositiveInt, PositiveInt] = (1, 10)
    mysql_host: Union[str, IPv4Address] = '127.0.0.1'
    mysql_port: PositiveInt = '3306'
    mysql_user: str
    mysql_password: SecretStr
    mysql_database: str
    mysql_connections_count: Tuple[PositiveInt, PositiveInt] = (1, 10)

    class Config:
        """Конфигурация настроек."""

        env_file = str(BASE_DIRECTORY_PATH / '.database.env')
        env_file_encoding = 'utf-8'


database_settings, application_settings = DatabaseSettings(), ApplicationSettings()
