"""Модуль приложения."""
import json
from pathlib import Path

import aiohttp_cors
from aiohttp.web_app import Application

from time_tracker import views
from time_tracker.databases import close_mysql, close_redis, init_mysql, init_redis
from time_tracker.middlewares import setup_middlewares
from time_tracker.settings import application_settings, database_settings


async def _create_logs_file(application: Application):
    """Создание файла логирования если он отсутствует."""
    log_file_path: Path = application['settings'].log_file_path
    if log_file_path.exists():
        return
    with log_file_path.open(mode='x') as log_file:
        json.dump({'items': []}, log_file)


async def create_application() -> Application:
    """Создание WEB приложения."""
    application = Application()
    application['database_settings'] = database_settings
    application['settings'] = application_settings

    cors_options = aiohttp_cors.ResourceOptions(expose_headers='*', allow_headers='*')
    aiohttp_cors.setup(application, defaults={'*': cors_options})

    application.add_routes(views.routes)
    setup_middlewares(application)

    application.on_startup.append(init_mysql)
    application.on_cleanup.append(close_mysql)
    application.on_startup.append(init_redis)
    application.on_cleanup.append(close_redis)
    application.on_startup.append(_create_logs_file)

    return application
