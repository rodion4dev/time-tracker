"""Модуль БД."""
import aiomysql
from aiohttp.web_app import Application

from time_tracker.settings import _DatabaseSettings


async def init_mysql(application: Application):
    """Подготовка MySQL."""
    settings: _DatabaseSettings = application['database_settings']
    minsize, maxsize = settings.mysql_connections_count
    connections_pool: aiomysql.Pool = await aiomysql.create_pool(
        minsize=minsize, maxsize=maxsize, host=settings.mysql_host,
        user=settings.mysql_user, password=settings.mysql_password.get_secret_value(),
        db=settings.mysql_database, port=settings.mysql_port, charset='utf8',
        program_name='time_tracker')
    application['mysql_connections_pool'] = connections_pool


async def close_mysql(application: Application):
    """Закрытие соединений MySQL."""
    connections_pool: aiomysql.Pool = application['mysql_connections_pool']
    connections_pool.close()
    await connections_pool.wait_closed()


async def init_redis(application: Application):
    """Подготовка Redis."""


async def close_redis(application: Application):
    """Подготовка Redis."""
