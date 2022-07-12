from uuid import UUID

from .repositories import FilmRatingRepository
from .types import FilmAverageRating, FilmRating


class FilmRatingService:
    """Сервис для работы с рейтингом фильма."""

    def __init__(self, film_rating_repository: FilmRatingRepository) -> None:
        assert isinstance(film_rating_repository, FilmRatingRepository)
        self._repository = film_rating_repository

    async def add_rating(self, rating: FilmRating) -> FilmRating:
        """Добавление пользовательского рейтинга/оценки к фильму."""
        return await self._repository.create(rating)

    async def get_film_rating(self, film_id: UUID, /) -> FilmAverageRating:
        """Получение среднего значения рейтинга фильма."""
        average_rating = await self._repository.get_by_film_id(str(film_id))
        return average_rating
