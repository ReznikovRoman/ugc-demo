from contextlib import suppress
from typing import Sequence

from aioredis import RedisError
from aredis_om import NotFoundError as RedisNotFoundError

from ugc.common.exceptions import NotFoundError
from ugc.infrastructure.db.repositories import BaseRepository

from . import types
from .factories import FilmBookmarkFactory
from .models import FilmBookmark


class BookmarkRepository(BaseRepository[FilmBookmark]):
    """Репозиторий для работы с данными закладок."""

    model = FilmBookmark

    def __init__(self, bookmark_factory: FilmBookmarkFactory) -> None:
        assert isinstance(bookmark_factory, FilmBookmarkFactory)
        self._factory = bookmark_factory

    async def create(self, bookmark: types.FilmBookmark, /) -> types.FilmBookmark:
        """Создание новой закладки."""
        data = bookmark.to_dict()
        data.pop("id", None)
        data.pop("bookmarked")
        obj = await self.model(**data).save()
        bookmark.id = obj.pk
        return bookmark

    async def get_by_user_id(self, user_id: str) -> list[types.FilmBookmark]:
        """Получения списка закладок пользователя по его ID."""
        bookmarks = await self.model.find(self.model.user_id == user_id).all()
        return self._deserialize_sequence(bookmarks)

    async def get_by_film_id(self, *, user_id: str, film_id: str) -> types.FilmBookmark:
        """Получение закладки пользователя по id фильма."""
        try:
            obj = await self.model.find(
                (self.model.user_id == user_id) &
                (self.model.film_id == film_id),
            ).first()
            data = obj.dict()
            data["id"] = data.pop("pk")
            data["bookmarked"] = True
            return self._factory.create_from_serialized(data)
        except RedisNotFoundError:
            raise NotFoundError()

    async def delete(self, *, user_id: str, film_id: str) -> None:
        """Удаление закладки."""
        # XXX: клиент Redis OM не обрабатывает корректно ошибки при `.delete()` [1]
        # [1] https://github.com/redis/redis-om-python/blob/d604797d9d01c06ff9268d1c4e644c20da6340d4/aredis_om/model/model.py#L794  # noqa
        with suppress(RedisError):
            return await self.model.find(
                (self.model.user_id == user_id) &
                (self.model.film_id == film_id),
            ).delete()

    def _deserialize_sequence(self, bookmarks: Sequence[FilmBookmark]) -> list[types.FilmBookmark]:
        deserialized = [
            self._factory.create_from_serialized(self._prepare_fields(bookmark))
            for bookmark in bookmarks
        ]
        return deserialized

    @staticmethod
    def _prepare_fields(bookmark: FilmBookmark) -> dict:
        data = bookmark.dict()
        data["id"] = str(data.pop("pk"))
        data["bookmarked"] = True
        return data
