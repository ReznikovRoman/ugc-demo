from typing import ClassVar
from uuid import UUID

from ugc.infrastructure.db.types import PaginationCursor

from .factories import FilmReviewFactory
from .repositories import ReviewRepository
from .types import FilmReview


class ReviewService:
    """Сервис для работы с рецензиями."""

    DEFAULT_REVIEWS_PAGE_SIZE: ClassVar[int] = 3

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

    async def get_film_reviews(
        self, film_id: UUID, *, limit: int | None = None, cursor: PaginationCursor = None,
    ) -> tuple[list[FilmReview], PaginationCursor]:
        """Получение списка рецензий на фильм."""
        if limit is None:
            limit = self.DEFAULT_REVIEWS_PAGE_SIZE
        reviews = await self._repository.get_paginated(str(film_id), limit=limit, cursor=cursor)
        return reviews
