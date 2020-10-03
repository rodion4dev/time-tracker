"""Модуль приложения."""
from aiohttp.web_app import Application

from time_tracker import views
from time_tracker.settings import application_settings, database_settings


async def create_application() -> Application:
    """Создание WEB приложения."""
    application = Application()
    application['settings'] = application_settings
    application['database_settings'] = database_settings
    application.add_routes(views.routes)

    return application
