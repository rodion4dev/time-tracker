"""Модуль приложения."""
from aiohttp.web_app import Application


async def create_application() -> Application:
    """Создание WEB приложения."""
    return Application()
