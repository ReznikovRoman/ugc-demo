from typing import Any
from uuid import UUID

from ugc.helpers import delay_tasks
from ugc.infrastructure.queue.producers import AsyncProducer

from .factories import FilmRatingFactory
from .types import FilmRating


class FilmRatingDispatcherService:
    """Сервис для диспатчинга событий рейтинга фильма."""

    def __init__(self, film_rating_factory: FilmRatingFactory, producer: AsyncProducer, config: dict[str, Any]) -> None:
        assert isinstance(film_rating_factory, FilmRatingFactory)
        self._film_rating_factory = film_rating_factory

        assert isinstance(producer, AsyncProducer)
        self._producer = producer

        assert isinstance(config, dict)
        self._config = config

    async def dispatch_film_rating(self, *, user_id: UUID, film_id: UUID, rating: int) -> FilmRating:
        film_rating = self._film_rating_factory.create_new(user_id=user_id, film_id=film_id, rating=rating)
        delay_tasks(
            self._producer.send(
                self._config["QUEUE_FILM_RATING_NAME"], key=f"{user_id}:{film_id}", message=film_rating.to_dict(),
            ),
        )
        return film_rating
