import re
from uuid import UUID

from aioredis import Redis

from ugc.infrastructure.db.repositories import BaseRepository

from . import types
from .exceptions import NoFilmRatingError
from .factories import FilmRatingFactory
from .models import FilmRating


class FilmRatingRepository(BaseRepository[FilmRating]):
    """Репозиторий для работы с данными оценок фильмов."""

    model = FilmRating

    def __init__(self, redis_client: Redis, film_rating_factory: FilmRatingFactory) -> None:
        assert isinstance(redis_client, Redis)
        self._redis_client = redis_client

        assert isinstance(film_rating_factory, FilmRatingFactory)
        self._factory = film_rating_factory

    async def create(self, rating: types.FilmRating, /) -> types.FilmRating:
        """Добавление оценки пользователя для фильма."""
        await self.update_or_create(
            defaults={"rating": rating.rating},
            user_id=str(rating.user_id),
            film_id=str(rating.film_id),
        )
        return rating

    async def get_by_film_id(self, film_id: str, /) -> types.FilmAverageRating:
        """Получение средней оценки фильма по его ID."""
        escaped_film_id = re.escape(film_id)
        # Redis Aggregations: https://redis.io/docs/stack/search/reference/aggregations/
        average_rating_raw = await self._redis_client.execute_command(
            f"FT.AGGREGATE ugc:ugc.domain.ratings.models.FilmRating:index "
            f"@film_id:{{{escaped_film_id}}} GROUPBY 1 @film_id REDUCE AVG 1 @rating",
        )
        average_rating = self._format_rating_aggregation(average_rating_raw)
        data = {"film_id": UUID(film_id), "rating": average_rating}
        return types.FilmAverageRating.from_dict(data)

    @staticmethod
    def _format_rating_aggregation(raw_result: list) -> float:
        if not raw_result[0]:
            raise NoFilmRatingError()
        average_rating = float(raw_result[1][-1])
        return round(average_rating, 2)
