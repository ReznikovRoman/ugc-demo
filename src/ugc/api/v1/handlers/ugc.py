from http import HTTPStatus

from aiohttp_apispec import docs

from aiohttp import web

from ugc.api.security import get_user_id


@docs(
    tags=["bookmarks"],
    summary="Добавить фильм в закладки.",
    responses={
        HTTPStatus.ACCEPTED: {"description": "Фильм добавлен в закладки"},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера"},
    },
)
async def bookmark_film(request: web.Request) -> web.Response:
    """Добавление фильма с `film_id` в закладки авторизованному пользователю."""
    user_id = get_user_id(request)
    print('user_id',user_id)
    return web.json_response(status=HTTPStatus.ACCEPTED)


@docs(
    summary="Получить список фильмов в закладках.",
    tags=["bookmarks"],
    responses={
        HTTPStatus.OK: {"description": "Ok"},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера"},
    },
)
async def bookmark_films(request: web.Request) -> web.Response:
    """Получение списка фильмов в закладках авторизованного пользователя"""
    # TODO get films_list from repository filtered by request.user["id"]
    user_id = get_user_id(request)
    print('user_id',user_id)
    bookmark_films_list = {"XXX":"XXX"}
    return web.json_response(bookmark_films_list, status=HTTPStatus.OK)


@docs(
    tags=["progress"],
    summary="Установить прогресс фильма для пользователя.",
    responses={
        HTTPStatus.OK: {"description": "Ok"},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера"},
    },
)
async def set_film_progress(request: web.Request) -> web.Response:
    user_id = get_user_id(request)
    print('user_id',user_id)
    return web.json_response(status=HTTPStatus.OK)


@docs(
    tags=["progress"],
    summary="Получить прогресс фильма для пользователя.",
    responses={
        HTTPStatus.OK: {"description": "Ok"},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера"},
    },
)
async def get_film_progress(request: web.Request) -> web.Response:
    user_id = get_user_id(request)
    print('user_id',user_id)
    return web.json_response(status=HTTPStatus.OK)
