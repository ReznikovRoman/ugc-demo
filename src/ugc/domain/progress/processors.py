from ugc.infrastructure.queue.typedefs import IConsumerRecord

from .factories import FilmProgressFactory
from .repositories import FilmProgressRepository
from .types import FilmProgress


class ProgressProcessor:
    """Обработка сообщения о трекинге фильма."""

    def __init__(self, progress_factory: FilmProgressFactory, progress_repository: FilmProgressRepository) -> None:
        assert isinstance(progress_factory, FilmProgressFactory)
        self._factory = progress_factory

        assert isinstance(progress_repository, FilmProgressRepository)
        self._repository = progress_repository

    async def __call__(self, message: IConsumerRecord) -> FilmProgress:
        progress = self._factory.create_from_serialized(message.value)
        await self._repository.track_progress(progress)
        return progress
