from pymongo.errors import DuplicateKeyError

from ugc.common.exceptions import ConflictError
from ugc.infrastructure.db.clients import MongoDatabaseClient

from .types import FilmReview


class ReviewRepository:
    """Репозиторий для работы с данными рецензий."""

    def __init__(self, db: MongoDatabaseClient) -> None:
        assert isinstance(db, MongoDatabaseClient)
        self._db = db

    async def create(self, /, review: FilmReview) -> FilmReview:
        """Создание рецензии."""
        try:
            review_db = await self._db["reviews"].insert_one(review.to_dict())
        except DuplicateKeyError:
            raise ConflictError(message=f"User has already written a review for film {review.film_id}.")
        review.id = str(review_db.inserted_id)
        return review
