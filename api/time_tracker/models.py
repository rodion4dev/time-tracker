"""Модели проекта."""
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union

import aiomysql
from aioredis import Redis
from pydantic import BaseModel


class Manager(ABC):
    """Менеджер данных базы."""

    database: Any

    def __init__(self, database: Any):
        """Конструктор менеджера."""
        self.database = database

    @abstractmethod
    async def save(self, model_object: 'Model'):
        """Сохранение указанного объекта."""
        raise NotImplementedError('Метод не реализован.')

    @abstractmethod
    async def get(self, key: str) -> 'Model':
        """Получение объекта по указанному ключу."""
        raise NotImplementedError('Метод не реализован.')

    @abstractmethod
    async def get_all(self) -> List['Model']:
        """Получение всех данных из базы."""
        raise NotImplementedError('Метод не реализован.')


class RedisManager(Manager):
    """Менеджер данных Redis."""

    database: Redis

    async def save(self, model_object: 'RedisData'):
        """
        Сохранение указанного объекта.

        Важно! Метод является идемпотентным: то есть его повторный вызов не вызовет
        исключение и обновит данные в базе по ключу объекта.
        """
        await self.database.set(model_object.key, model_object.value)

    async def get(self, key: str) -> Optional['RedisData']:
        """Получение объекта по указанному ключу."""
        value = await self.database.get(key)
        if value:
            return RedisData(key=key, value=value)

    async def get_all(self) -> List['RedisData']:
        """Получение всех данных из базы."""
        redis_data_list = []
        for key in await self.database.keys('*'):
            value = await self.database.get(key)
            redis_data_list.append(RedisData(key=key, value=value))
        return redis_data_list


class MySQLManager(Manager):
    """Менеджер данных MySQL."""

    database: aiomysql.Pool


class Model(BaseModel, ABC):
    """Модель данных с доступом к базе."""

    async def save(self, database: Union[Redis, aiomysql.Pool]):
        """Сохранение данных используя указанную базу."""
        manager = self.get_manager(database)
        await manager.save(self)

    @staticmethod
    async def get(key: str, database: Union[Redis, aiomysql.Pool]):
        """Получение данных из указанной базы."""
        manager = Model.get_manager(database)
        return await manager.get(key)

    @staticmethod
    async def get_all(database: Union[Redis, aiomysql.Pool]):
        """Получение всех данных из указанной базы."""
        manager = Model.get_manager(database)
        return await manager.get_all()

    @staticmethod
    def get_manager(database: Union[Redis, aiomysql.Pool]) -> Manager:
        """Получение менеджера для указанной базы данных."""
        managers = {Redis: RedisManager, aiomysql.Pool: MySQLManager}
        manager = managers.get(database.__class__)
        if not manager:
            raise ValueError(
                f'Данная операция для {database.__class__} не поддерживается.'
            )
        return manager(database)


class RedisData(Model):
    """Redis данные."""

    key: str
    value: str
