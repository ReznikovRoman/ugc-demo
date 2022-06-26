from uuid import UUID

from .repositories import FilmProgressRepository
from .types import FilmProgress


class ProgressService:
    """Сервис для работы с прогрессом фильма."""

    def __init__(self, progress_repository: FilmProgressRepository) -> None:
        assert isinstance(progress_repository, FilmProgressRepository)
        self._repository = progress_repository

    async def get_film_progress_for_user(self, *, user_id: UUID, film_id: UUID) -> FilmProgress:
        progress = await self._repository.get_by_film_id(user_id=str(user_id), film_id=str(film_id))
        return progress
