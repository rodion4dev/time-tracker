"""Модуль БД."""
import aiomysql
import aioredis
from aiohttp.web_app import Application

from time_tracker.settings import _DatabaseSettings


async def init_mysql(application: Application):
    """Подготовка MySQL."""
    settings: _DatabaseSettings = application['database_settings']
    minsize, maxsize = settings.mysql_connections_count
    mysql_pool: aiomysql.Pool = await aiomysql.create_pool(
        minsize=minsize,
        maxsize=maxsize,
        host=settings.mysql_host,
        user=settings.mysql_user,
        password=settings.mysql_password.get_secret_value(),
        db=settings.mysql_database,
        port=settings.mysql_port,
        charset='utf8',
        program_name='time_tracker',
    )
    application['mysql_pool'] = mysql_pool


async def close_mysql(application: Application):
    """Закрытие соединений MySQL."""
    mysql_pool: aiomysql.Pool = application['mysql_pool']
    mysql_pool.close()
    await mysql_pool.wait_closed()


async def init_redis(application: Application):
    """Подготовка Redis."""
    settings: _DatabaseSettings = application['database_settings']
    minsize, maxsize = settings.redis_connections_count
    redis: aioredis.Redis = await aioredis.create_redis_pool(
        settings.redis_dsn, encoding='utf-8', minsize=minsize, maxsize=maxsize
    )
    application['redis_pool'] = redis


async def close_redis(application: Application):
    """Закрытие соединений Redis."""
    redis: aioredis.Redis = application['redis_pool']
    redis.close()
    await redis.wait_closed()
