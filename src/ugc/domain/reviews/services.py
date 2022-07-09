from uuid import UUID

from .factories import FilmReviewFactory
from .repositories import ReviewRepository
from .types import FilmReview


class ReviewService:
    """Сервис для работы с рецензиями."""

    def __init__(self, review_factory: FilmReviewFactory, review_repository: ReviewRepository) -> None:
        assert isinstance(review_factory, FilmReviewFactory)
        self._factory = review_factory

        assert isinstance(review_repository, ReviewRepository)
        self._repository = review_repository

    async def create_review(self, *, user_id: UUID, film_id: UUID, title: str, review_text: str) -> FilmReview:
        """Создание новой рецензии на фильм."""
        review_dto = self._factory.create_new(user_id=user_id, film_id=film_id, title=title, review=review_text)
        review = await self._repository.create(review_dto)
        return review
