# Серверная часть приложения учёта времени

## Рекомендации к окружению
* pipenv (рекомендуется) или venv модуль
* python версии 3.6 или выше
* развёрнутое виртуальное окружение с установленными зависимостями из requirements.txt

## Переменные окружения (.application.env & .database.env)
* LOG_FILE_PATH: Путь до json файла с логированием (приложение создаст автоматически)
* REDIS_DSN: URL до базы данных Redis (по-умолчанию: redis://127.0.0.1:6379/0)
* REDIS_CONNECTIONS_COUNT: Количество допустимых соединений с Redis (по-умолчанию: [1,10])
* MYSQL_HOST: Имя хоста с базой данных MySQL (по-умолчанию: 127.0.0.1)
* MYSQL_PORT: Номер порта MySQL (по-умолчанию: 3306)
* MYSQL_USER: Имя пользователя для соединения с базой данных
* MYSQL_PASSWORD: Пароль пользователя для соединения с базой данных
* MYSQL_DATABASE: Имя базы данных
* MYSQL_CONNECTIONS_COUNT: Количество допустимых соединений с MySQL (по-умолчанию: [1,10])

## Запуск приложения (на основе aiohttp)

Для разработки:
```shell script
python3 -m time_tracker
```

Для развёртывания в боевом окружении:
```shell script
python3 -m time_tracker --socket_path <путь до unix-сокета>
```
Подробнее про развёртывание: https://docs.aiohttp.org/en/stable/deployment.html#nginx-supervisord

## Доступные рабочие запросы:

* GET /redis-data/{key}: получение Redis данных по ключу key
* POST /redis-data: сохранение данных в Redis
  * Тело запроса
    ```json
    {
      "key": "ключ",
      "value": "значение ключа"
    }
    ```
