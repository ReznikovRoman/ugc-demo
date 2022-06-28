from http import HTTPStatus

from . import serializers

add_film_bookmark = {
    "tags": ["bookmarks"],
    "summary": "Добавить фильм в закладки.",
    "security": [{"JWT": []}],
    "responses": {
        HTTPStatus.ACCEPTED: {"description": "Фильм добавлен в закладки пользователя."},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
}

get_user_films_bookmarks = {
    "tags": ["bookmarks"],
    "summary": "Получить список фильмов в закладках.",
    "security": [{"JWT": []}],
    "responses": {
        HTTPStatus.OK: {
            "description": "Список фильмов в закладках пользователя.",
            "schema": serializers.FilmBookmarkList(many=True),
        },
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
}

track_film_progress = {
    "tags": ["progress"],
    "summary": "Установить прогресс фильма для пользователя.",
    "security": [{"JWT": []}],
    "responses": {
        HTTPStatus.ACCEPTED: {"description": "Прогресс фильма сохранен."},
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
}

get_film_progress = {
    "tags": ["progress"],
    "summary": "Получить прогресс фильма для пользователя.",
    "security": [{"JWT": []}],
    "responses": {
        HTTPStatus.OK: {
            "description": "Прогресс фильма.",
            "schema": serializers.FilmProgressDetail,
        },
        HTTPStatus.UNAUTHORIZED: {"description": "Пользователь не авторизован."},
        HTTPStatus.NOT_FOUND: {"description": "Прогресс для данного фильма не найден."},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"description": "Ошибка сервера."},
    },
}