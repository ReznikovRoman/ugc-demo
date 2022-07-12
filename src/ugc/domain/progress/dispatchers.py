from typing import Any
from uuid import UUID

from ugc.helpers import delay_tasks
from ugc.infrastructure.queue.producers import AsyncProducer

from .factories import FilmProgressFactory
from .types import FilmProgress


class ProgressDispatcherService:
    """Сервис для диспатчинга событий о прогрессе фильма."""

    def __init__(self, progress_factory: FilmProgressFactory, producer: AsyncProducer, config: dict[str, Any]) -> None:
        assert isinstance(progress_factory, FilmProgressFactory)
        self._factory = progress_factory

        assert isinstance(producer, AsyncProducer)
        self._producer = producer

        assert isinstance(config, dict)
        self._config = config

    async def dispatch_progress_tracking(self, *, user_id: UUID, film_id: UUID, viewed_frame: int) -> FilmProgress:
        progress = self._factory.create_new(user_id=user_id, film_id=film_id, viewed_frame=viewed_frame)
        delay_tasks(
            self._producer.send(
                self._config["QUEUE_PROGRESS_NAME"], key=f"{user_id}:{film_id}", message=progress.to_dict(),
            ),
        )
        return progress
