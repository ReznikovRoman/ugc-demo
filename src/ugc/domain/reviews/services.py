from .repositories import ReviewRepository


class ReviewService:
    """Сервис для работы с рецензиями."""

    def __init__(self, review_repository: ReviewRepository) -> None:
        assert isinstance(review_repository, ReviewRepository)
        self._repository = review_repository

    async def create_review(self):
        """Создание новой рецензии на фильм."""
        await self._repository.create()
