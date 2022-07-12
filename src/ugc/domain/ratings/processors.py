from ugc.infrastructure.queue.typedefs import IConsumerRecord

from .factories import FilmRatingFactory
from .services import FilmRatingService
from .types import FilmRating


class FilmRatingProcessor:
    """Обработка добавления оценок фильма."""

    def __init__(self, film_rating_factory: FilmRatingFactory, film_rating_service: FilmRatingService) -> None:
        assert isinstance(film_rating_factory, FilmRatingFactory)
        self._factory = film_rating_factory

        assert isinstance(film_rating_service, FilmRatingService)
        self._service = film_rating_service

    async def __call__(self, message: IConsumerRecord) -> FilmRating:
        rating = self._factory.create_from_serialized(message.value)
        await self._service.add_rating(rating)
        return rating
