"""Набор обработчиков HTTP запросов."""
import json
from pathlib import Path

from aiohttp.web_response import Response, json_response
from aiohttp.web_routedef import RouteTableDef
from aiohttp.web_urldispatcher import View
from aioredis import Redis
from aioredis.commands import StringCommandsMixin

routes = RouteTableDef()


@routes.view('/logs')
class LogView(View):
    """Взаимодействие с логами."""

    async def get(self) -> Response:
        """Получение логов."""
        log_file_path: Path = self.request.app['settings'].log_file_path
        with log_file_path.open(encoding='utf-8') as logs_file:
            return json_response(data=json.load(logs_file))


@routes.view('/mysql-data')
class MySQLData(View):
    """Взаимодействие с данными в MySQL базе."""

    async def get(self) -> Response:
        """Получение данных из MySQL."""
        return json_response(data={})

    async def post(self) -> Response:
        """Сохранение данных в MySQL."""
        return json_response(data={})


@routes.view('/redis-data')
class RedisData(View):
    """Обработка Redis данных."""

    async def get(self) -> Response:
        """Получение всех данных из Redis."""
        redis: Redis = self.request.app['redis']
        all_data = {}
        for key in await redis.keys('*'):
            all_data[key] = await redis.get(key)
        return json_response(data=all_data)

    async def post(self) -> Response:
        """Сохранение данных в Redis."""
        data = await self.request.json()
        if not isinstance(data, dict):
            return json_response(data={'error': 'Ожидался объект с данными.'})

        redis: Redis = self.request.app['redis']
        for key, value in data.items():
            await redis.set(key, value, exist=StringCommandsMixin.SET_IF_NOT_EXIST)
        return json_response(data=data)
