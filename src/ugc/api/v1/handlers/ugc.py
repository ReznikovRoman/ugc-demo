from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from uuid import UUID

from aiohttp_apispec import docs
from dependency_injector.wiring import Provide, inject

from aiohttp import web

from ugc.api.security import get_user_id_from_jwt
from ugc.api.utils import orjson_response
from ugc.api.v1 import openapi
from ugc.containers import Container

if TYPE_CHECKING:
    from ugc.domain.bookmarks import BookmarkService
    from ugc.domain.progress import ProgressService


@docs(**openapi.add_film_bookmark)
async def add_film_bookmark(request: web.Request) -> web.Response:
    """Добавление фильма с `film_id` в закладки авторизованному пользователю."""
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    # TODO: user_id, film_id нужны для задачи https://github.com/ReznikovRoman/netflix-ugc/issues/9
    print("user_id", user_id, "film_id", film_id)
    return orjson_response(status=HTTPStatus.ACCEPTED)


@docs(**openapi.get_user_films_bookmarks)
@inject
async def get_user_films_bookmarks(
    request: web.Request, *,
    bookmark_service: BookmarkService = Provide[Container.bookmark_service],
) -> web.Response:
    """Получение списка фильмов в закладках авторизованного пользователя."""
    user_id = get_user_id_from_jwt(request.headers)
    bookmarks = await bookmark_service.get_user_bookmarks(user_id)
    return orjson_response(bookmarks, status=HTTPStatus.OK)


@docs(**openapi.track_film_progress)
async def track_film_progress(request: web.Request) -> web.Response:
    """Сохранение прогресса фильма с `film_id` для авторизованного пользователя."""
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    print("user_id", user_id, "film_id", film_id)
    # TODO: user_id, film_id нужны для задачи https://github.com/ReznikovRoman/netflix-ugc/issues/9
    return orjson_response(status=HTTPStatus.OK)


@docs(**openapi.get_film_progress)
@inject
async def get_film_progress(
    request: web.Request, *,
    progress_service: ProgressService = Provide[Container.progress_service],
) -> web.Response:
    """Получение прогресса фильма с `film_id` для авторизованного пользователя."""
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    progress = await progress_service.get_user_film_progress(user_id=user_id, film_id=film_id)
    return orjson_response(progress, status=HTTPStatus.OK)
