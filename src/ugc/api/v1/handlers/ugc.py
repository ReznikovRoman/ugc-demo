from http import HTTPStatus
from uuid import UUID

from aiohttp_apispec import docs

from aiohttp import web

from ugc.api.security import get_user_id_from_jwt
from ugc.api.utils import orjson_response


@docs(
    tags=["bookmarks"],
    summary="Добавить фильм в закладки.",
    security=[{"JWT": []}],
    responses={
        HTTPStatus.ACCEPTED: {"description": "Фильм добавлен в закладки пользователя."},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
)
async def add_film_bookmark(request: web.Request) -> web.Response:
    """Добавление фильма с `film_id` в закладки авторизованному пользователю."""
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    # TODO: user_id, film_id нужны для задачи https://github.com/ReznikovRoman/netflix-ugc/issues/9
    print("user_id", user_id, "film_id", film_id)
    return orjson_response(status=HTTPStatus.ACCEPTED)


@docs(
    summary="Получить список фильмов в закладках.",
    tags=["bookmarks"],
    security=[{"JWT": []}],
    responses={
        HTTPStatus.OK: {"description": "Список фильмов в закладках пользователя."},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
)
async def get_user_films_bookmarks(request: web.Request) -> web.Response:
    """Получение списка фильмов в закладках авторизованного пользователя."""
    user_id = get_user_id_from_jwt(request.headers)
    # TODO: user_id нужен для задачи https://github.com/ReznikovRoman/netflix-ugc/issues/10
    print("user_id", user_id)
    bookmark_films_list = {"XXX": "XXX"}
    return orjson_response(bookmark_films_list, status=HTTPStatus.OK)


@docs(
    tags=["progress"],
    summary="Установить прогресс фильма для пользователя.",
    security=[{"JWT": []}],
    responses={
        HTTPStatus.OK: {"description": "Прогресс фильма сохранен."},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
)
async def track_film_progress(request: web.Request) -> web.Response:
    """Сохранение прогресса фильма с `film_id` для авторизованного пользователя."""
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    print("user_id", user_id, "film_id", film_id)
    # TODO: user_id, film_id нужны для задачи https://github.com/ReznikovRoman/netflix-ugc/issues/9
    return orjson_response(status=HTTPStatus.OK)


@docs(
    tags=["progress"],
    summary="Получить прогресс фильма для пользователя.",
    security=[{"JWT": []}],
    responses={
        HTTPStatus.OK: {"description": "Прогресс фильма."},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
)
async def get_film_progress(request: web.Request) -> web.Response:
    """Получение прогресса фильма с `film_id` для авторизованного пользователя."""
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    print("user_id", user_id, "film_id", film_id)
    # TODO: user_id, film_id нужны для задачи https://github.com/ReznikovRoman/netflix-ugc/issues/10
    return orjson_response(status=HTTPStatus.OK)
