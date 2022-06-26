from ugc.infrastructure.queue.typedefs import IConsumerRecord

from .factories import FilmProgressFactory
from .services import ProgressService
from .types import FilmProgress


class ProgressProcessor:
    """Обработка сообщения о трекинге фильма."""

    def __init__(self, progress_factory: FilmProgressFactory, progress_service: ProgressService) -> None:
        assert isinstance(progress_factory, FilmProgressFactory)
        self._factory = progress_factory

        assert isinstance(progress_service, ProgressService)
        self._service = progress_service

    async def __call__(self, message: IConsumerRecord) -> FilmProgress:
        progress = self._factory.create_from_serialized(message.value)
        await self._service.track_film_progress(progress)
        return progress
