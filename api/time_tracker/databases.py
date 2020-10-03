"""Модуль БД."""
import aiomysql
from aiohttp.web_app import Application
from aiomysql import Connection

from time_tracker.settings import _DatabaseSettings


async def init_mysql(application: Application):
    """Подготовка MySQL базы данных."""
    settings: _DatabaseSettings = application['database_settings']
    application['mysql_connection']: Connection = await aiomysql.connect()


async def close_mysql(application: Application):
    """Закрытие соединения с MySQL базой данных."""
    mysql_connection: Connection = application['mysql_connection']
    mysql_connection.close()
    await mysql_connection.ensure_closed()
