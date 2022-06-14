# Netflix UGC
Сервис для работы с пользовательским контентом.

## Технологии
- aiohttp
  - [aiohttp-apispec](https://aiohttp-apispec.readthedocs.io/en/latest/)
    - Swagger docs
- Redis (Redis Stack on Redis Enterprise)
  - Основное хранилище пользовательского контента
- Clickhouse
  - OLAP DMS
- Kafka
  - Платформа для стриминга событий
  - Используется в качестве engine в ClickHouse

## АПИ
- Авторизированный пользователь
  - Добавление фильма `film_id` в закладки пользователя
    - `POST /api/v1/users/me/bookmarks/films/{film_id}`
  - Получение списка закладок по фильмам для пользователя
    - `GET /api/v1/users/me/bookmarks/films`
  - Трекинг прогресса фильма `film_id` для пользователя
    - `POST /api/v1/users/me/progress/films/{film_id}`
    - Тело запроса
      ```json
        {
          "viewed_frame": 123.412
        }
      ```
  - \* Получение прогресса фильма `film_id` для пользователя
    - `GET /api/v1/users/me/progress/films/{film_id}`
