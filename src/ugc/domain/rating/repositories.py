from contextlib import suppress
from typing import Sequence

from aioredis import RedisError

from ugc.common.exceptions import NotFoundError
from ugc.infrastructure.db.repositories import BaseRepository

from . import types
from .factories import FilmRatingFactory
from .models import FilmRating


class FilmRatingRepository(BaseRepository[FilmRating]):
    """Репозиторий для работы с данными оценок фильмов."""

    model = FilmRating

    def __init__(self, film_rating_factory: FilmRatingFactory) -> None:
        assert isinstance(film_rating_factory, FilmRatingFactory)
        self._factory = film_rating_factory

    async def create(self, rating: types.FilmRating, /) -> types.FilmRating:
        """Добавление оценки пользователя для фильма."""
        data = rating.to_dict()
        rating = await self.model(**data).save()
        return rating

    async def get_by_user_id(self, user_id: str) -> list[types.FilmRating]:
        """Получение списка оценок пользователя по его ID."""
        film_ratings = await self.model.find(self.model.user_id == user_id).all()
        return self._deserialize_sequence(film_ratings)

    async def get_by_film_id(self, *, film_id: str) -> int:
        """Получение средней оценки фильма по его ID."""
        film_ratings = await self.model.find(self.model.film_id == film_id).all()
        rating_count = len(film_ratings)
        if rating_count:
            rating_sum = sum([film_rating.rating for film_rating in film_ratings])
            return rating_sum // rating_count
        raise NotFoundError()

    async def delete(self, *, user_id: str, film_id: str) -> None:
        """Удаление оценки."""
        # XXX: клиент Redis OM не обрабатывает корректно ошибки при `.delete()` [1]
        # [1] https://github.com/redis/redis-om-python/blob/d604797d9d01c06ff9268d1c4e644c20da6340d4/aredis_om/model/model.py#L794  # noqa
        with suppress(RedisError):
            return await self.model.find(
                (self.model.user_id == user_id) &
                (self.model.film_id == film_id),
            ).delete()

    def _deserialize_sequence(self, film_ratings: Sequence[FilmRating]) -> list[types.FilmRating]:
        deserialized = [
            self._factory.create_from_serialized(self._prepare_fields(film_rating))
            for film_rating in film_ratings
        ]
        return deserialized

    @staticmethod
    def _prepare_fields(film_rating: FilmRating) -> dict:
        data = film_rating.dict()
        data["id"] = str(data.pop("pk"))
        return data
