"""Набор обработчиков HTTP запросов."""
from aiohttp.web_response import Response, json_response
from aiohttp.web_routedef import RouteTableDef
from aiohttp.web_urldispatcher import View


routes = RouteTableDef()


@routes.view('/logs')
class LogView(View):
    """Взаимодействие с логами."""

    async def get(self) -> Response:
        """Получение логов."""
        return json_response(data={})


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
    """Взаимодействие с данными в Redis базе."""

    async def get(self) -> Response:
        """Получение данных из Redis."""
        return json_response(data={})

    async def post(self) -> Response:
        """Сохранение данных в Redis."""
        return json_response(data={})
