"""Middlewares."""
import json
from json import JSONDecodeError
from logging import getLogger
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List

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
        except Exception as unknown_error:
            getLogger(__name__).error(
                f'При обработке запроса {request.method} {request.path} произошла '
                f'неизвестная ошибка: {unknown_error}'
            )
            override = overrides.get(500)
            return await override(request)

    return error_middleware


@middleware
async def _log_request(request: Request, handler: Handler) -> StreamResponse:
    response = await handler(request)
    log_file_path: Path = request.app['settings'].log_file_path
    with log_file_path.open(encoding='utf-8') as logs_file:
        logs: Dict[str, List[Dict[str, Any]]] = json.load(logs_file)
        try:
            data = await request.json()
        except JSONDecodeError:
            data = None
        logs['items'].append(
            {
                'response': {'code': response.status},
                'request': {
                    'data': data,
                    'method': request.method,
                    'path': request.path,
                },
            }
        )
    with log_file_path.open(mode='w', encoding='utf-8') as logs_file:
        json.dump(logs, logs_file)
    return response


def setup_middlewares(application: Application):
    """Добавление middlewares для указанного приложения."""
    error_middleware = _create_error_middleware({500: _notify_server_errors})
    application.middlewares.append(error_middleware)
    application.middlewares.append(_log_request)
