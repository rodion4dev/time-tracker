"""Настройки проекта."""
from ipaddress import IPv4Address
from pathlib import Path
from typing import Union

from pydantic import BaseSettings, PositiveInt, RedisDsn, SecretStr

BASE_DIRECTORY_PATH = Path(__file__).absolute().parent.parent


class _DatabaseSettings(BaseSettings):
    """Настройки баз данных."""

    redis_dsn: RedisDsn
    mysql_host: Union[str, IPv4Address] = 'localhost'
    mysql_port: PositiveInt = '3306'
    mysql_user: str
    mysql_password: SecretStr
    mysql_database: str

    class Config:
        """Мета конфигурация настроек."""

        env_file = str(BASE_DIRECTORY_PATH / '.database.env')
        env_file_encoding = 'utf-8'


class _ApplicationSettings(BaseSettings):
    """Прочие настройки приложения."""

    class Config:
        """Мета конфигурация настроек."""

        env_file = str(BASE_DIRECTORY_PATH / '.env')
        env_file_encoding = 'utf-8'


database_settings, application_settings = _DatabaseSettings(), _ApplicationSettings()
