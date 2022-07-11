from ugc.infrastructure.queue.typedefs import IConsumerRecord

from .factories import FilmRatingFactory
from .repositories import FilmRatingRepository
from .types import FilmRating


class FilmRatingProcessor:
    """Обработка добавления оценок фильма."""

    def __init__(self, film_rating_factory: FilmRatingFactory, film_rating_repository: FilmRatingRepository) -> None:
        assert isinstance(film_rating_factory, FilmRatingFactory)
        self._factory = film_rating_factory

        assert isinstance(film_rating_repository, FilmRatingRepository)
        self._repository = film_rating_repository

    async def __call__(self, message: IConsumerRecord) -> FilmRating:
        rating = self._factory.create_from_serialized(message.value)
        await self._repository.create(rating)
        return rating
