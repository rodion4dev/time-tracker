"""Модуль БД."""
import aiomysql
from aiohttp.web_app import Application

from time_tracker.settings import _DatabaseSettings


async def init_mysql(application: Application):
    """Подготовка MySQL базы данных."""
    settings: _DatabaseSettings = application['database_settings']
    connections_pool: aiomysql.Pool = await aiomysql.create_pool()
    application['mysql_connections_pool'] = connections_pool


async def close_mysql(application: Application):
    """Закрытие соединения с MySQL базой данных."""
    connections_pool: aiomysql.Pool = application['mysql_connections_pool']
    connections_pool.close()
    await connections_pool.wait_closed()
