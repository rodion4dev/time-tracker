"""Middlewares."""
from typing import Awaitable, Callable, Dict

from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPException
from aiohttp.web_middlewares import middleware
from aiohttp.web_request import Request
from aiohttp.web_response import Response, StreamResponse, json_response


async def _notify_server_errors(*args) -> Response:
    """Уведомление о серверных ошибках."""
    return json_response(
        data={'error': 'Ошибка на стороне сервера, попробуйте сделать запрос позднее.'},
        status=500,
    )


Handler = Callable[[Request], Awaitable[StreamResponse]]
Middleware = Callable[[Request, Handler], Awaitable[StreamResponse]]


def _create_error_middleware(overrides: Dict[int, Callable]) -> Middleware:
    """Создание middleware для обработки ошибок."""

    @middleware
    async def error_middleware(request: Request, handler: Callable):
        try:
            response: Response = await handler(request)
            if response.status >= 400:
                override = overrides.get(response.status)
                if override:
                    return await override(request)
            return response
        except HTTPException as error:
            override = overrides.get(error.status)
            if override:
                return await override(request)
            raise

    return error_middleware


def setup_middlewares(application: Application):
    """Добавление middlewares для указанного приложения."""
    error_middleware = _create_error_middleware({500: _notify_server_errors})
    application.middlewares.append(error_middleware)
