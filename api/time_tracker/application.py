"""Модуль приложения."""
from aiohttp.web_app import Application

from time_tracker import views


async def create_application() -> Application:
    """Создание WEB приложения."""
    application = Application()
    application.add_routes(views.routes)

    return application
