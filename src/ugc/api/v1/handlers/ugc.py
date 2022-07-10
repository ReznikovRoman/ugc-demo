from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING
from uuid import UUID

from aiohttp_apispec import docs, querystring_schema, request_schema
from dependency_injector.wiring import Provide, inject

from aiohttp import web

from ugc.api.security import get_user_id_from_jwt
from ugc.api.utils import orjson_response
from ugc.api.v1 import openapi, serializers
from ugc.containers import Container

if TYPE_CHECKING:
    from ugc.domain.bookmarks import BookmarkDispatcherService, BookmarkService
    from ugc.domain.progress import ProgressDispatcherService, ProgressService
    from ugc.domain.reviews import ReviewService


@docs(**openapi.add_film_bookmark)
@inject
async def add_film_bookmark(
    request: web.Request, *,
    bookmark_dispatcher: BookmarkDispatcherService = Provide[Container.bookmark_dispatcher_service],
) -> web.Response:
    """Добавление фильма с `film_id` в закладки авторизованному пользователю."""
    await _handle_film_bookmark(request, bookmark_dispatcher, bookmarked=True)
    return orjson_response(status=HTTPStatus.ACCEPTED)


@docs(**openapi.delete_film_bookmark)
@inject
async def delete_film_bookmark(
    request: web.Request, *,
    bookmark_dispatcher: BookmarkDispatcherService = Provide[Container.bookmark_dispatcher_service],
) -> web.Response:
    """Удаление фильма с `film_id` из закладок авторизованного пользователя."""
    await _handle_film_bookmark(request, bookmark_dispatcher, bookmarked=False)
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
@request_schema(serializers.FilmProgressCreate)
@inject
async def track_film_progress(
    request: web.Request, *,
    progress_dispatcher: ProgressDispatcherService = Provide[Container.progress_dispatcher_service],
) -> web.Response:
    """Сохранение прогресса фильма с `film_id` для авторизованного пользователя."""
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    validated_data = request["data"]
    viewed_frame = validated_data["viewed_frame"]
    await progress_dispatcher.dispatch_progress_tracking(user_id=user_id, film_id=film_id, viewed_frame=viewed_frame)
    return orjson_response(status=HTTPStatus.ACCEPTED)


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


@docs(**openapi.create_film_review)
@request_schema(serializers.FilmReviewCreate)
@inject
async def create_film_review(
    request: web.Request, *,
    review_service: ReviewService = Provide[Container.review_service],
) -> web.Response:
    """Создание новой рецензии на фильм от авторизированного пользователя."""
    data = request["data"]
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    review = await review_service.create_review(
        user_id=user_id, film_id=film_id, title=data["title"], review_text=data["review"])
    return orjson_response(review, status=HTTPStatus.CREATED)


@docs(**openapi.get_film_reviews)
@querystring_schema(serializers.CursorPaginationQueryParams)
@inject
async def get_film_reviews(
    request: web.Request, *,
    review_service: ReviewService = Provide[Container.review_service],
) -> web.Response:
    """Получение списка рецензий на фильм с пагинацией."""
    film_id: UUID = request.match_info["film_id"]
    query_params: dict = request["querystring"]
    reviews, cursor = await review_service.get_film_reviews(
        film_id, limit=query_params.get("limit"), cursor=query_params.get("cursor"))
    response = {"cursor": cursor, "data": reviews}
    return orjson_response(response, status=HTTPStatus.OK)


async def _handle_film_bookmark(
    request: web.Request,
    bookmark_dispatcher: BookmarkDispatcherService, *,
    bookmarked: bool,
) -> None:
    film_id: UUID = request.match_info["film_id"]
    user_id = get_user_id_from_jwt(request.headers)
    await bookmark_dispatcher.dispatch_bookmark_switch(user_id=user_id, film_id=film_id, bookmarked=bookmarked)
