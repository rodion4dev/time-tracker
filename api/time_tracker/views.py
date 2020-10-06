"""Набор обработчиков HTTP запросов."""
import json
from http.client import BAD_REQUEST, NOT_FOUND
from pathlib import Path

from aiohttp.web_request import Request
from aiohttp.web_response import Response, json_response
from aiohttp.web_routedef import RouteTableDef
from aiohttp.web_urldispatcher import View
from pydantic import ValidationError

from time_tracker.models import RedisData

routes = RouteTableDef()


@routes.view('/logs')
class LogDataView(View):
    """Обработка файла логирования."""

    async def get(self) -> Response:
        """Получение логов."""
        log_file_path: Path = self.request.app['settings'].log_file_path
        with log_file_path.open(encoding='utf-8') as logs_file:
            return json_response(data=json.load(logs_file))


@routes.view('/mysql-data')
class MySQLDataView(View):
    """Обработка данных MySQL."""

    async def get(self) -> Response:
        """Получение данных из MySQL."""
        return json_response(data={})

    async def post(self) -> Response:
        """Сохранение данных в MySQL."""
        return json_response(data={})


@routes.get('/redis-data/{key}')
async def get_redis_data(request: Request) -> Response:
    """Получение всех данных из Redis."""
    key = request.match_info['key']
    redis_data = await RedisData.get(key, request.app['redis'])
    if not redis_data:
        return json_response(
            data={'errors': [f'Объект с ключом {key} не найден.']},
            status=NOT_FOUND.value,
        )
    return json_response(data=dict(redis_data))


@routes.view('/redis-data')
class RedisDataView(View):
    """Взаимодействие с RedisData."""

    async def get(self) -> Response:
        """Получение всех данных из Redis."""
        redis_data_list = await RedisData.get_all(self.request.app['redis'])
        data = [dict(redis_data) for redis_data in redis_data_list]
        return json_response(data=data)

    async def post(self) -> Response:
        """Сохранение данных в Redis."""
        try:
            redis_data: RedisData = RedisData.parse_raw(await self.request.text())
        except ValidationError as error:
            return json_response(
                data={'errors': error.errors()}, status=BAD_REQUEST.value
            )

        await redis_data.save(self.request.app['redis'])
        return json_response(data=dict(redis_data))
