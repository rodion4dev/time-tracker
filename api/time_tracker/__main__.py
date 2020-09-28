"""
Основной модуль проекта для запуска команд.

Подробнее: https://docs.python.org/3/library/__main__.html
"""
import sys
from logging import getLogger
from pathlib import Path

import typer
from aiohttp.web import run_app

from time_tracker.application import create_application


def _run_application(socket_path: Path = None, port: int = None):
    """
    Запуск HTTP сервера с приложением.

    В зависимости от указанных параметров сервер принимает соединения либо через Unix
    сокет из socket_path, либо через TCP/IP соединение на указанный порт в параметре
    port.

    :param socket_path: путь до unix сокета
    :param port: номер порта
    """
    logger = getLogger(__name__)

    if socket_path and port:
        logger.error(
            'Не удалось запустить приложение: путь до сокета указан вместе с номером '
            'порта.'
        )
        sys.exit(1)
    if isinstance(socket_path, Path):
        socket_path = str(socket_path)

    run_app(create_application(), port=port, path=socket_path)


typer.run(_run_application)
