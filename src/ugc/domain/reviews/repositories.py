from typing import ClassVar

from bson import ObjectId
from pymongo import DESCENDING
from pymongo.errors import DuplicateKeyError

from ugc.common.exceptions import ConflictError
from ugc.infrastructure.db.clients import MongoDatabaseClient
from ugc.infrastructure.db.repositories import MongoRepository
from ugc.infrastructure.db.types import PaginationCursor

from .constants import REVIEWS_COLLECTION_NAME
from .factories import FilmReviewFactory
from .types import FilmReview


class ReviewRepository:
    """Репозиторий для работы с данными рецензий."""

    collection: ClassVar[str] = REVIEWS_COLLECTION_NAME

    def __init__(
        self, mongo_repository: MongoRepository[FilmReview], db: MongoDatabaseClient, review_factory: FilmReviewFactory,
    ) -> None:
        assert isinstance(mongo_repository, MongoRepository)
        self._mongo_repository = mongo_repository

        assert isinstance(db, MongoDatabaseClient)
        self._db = db

        assert isinstance(review_factory, FilmReviewFactory)
        self._factory = review_factory

    async def create(self, /, review: FilmReview) -> FilmReview:
        """Создание рецензии."""
        try:
            review_db = await self._db["reviews"].insert_one(review.to_dict())
        except DuplicateKeyError:
            raise ConflictError(message=f"User has already written a review for film {review.film_id}.")
        review.id = str(review_db.inserted_id)
        return review

    async def get_paginated(
        self, film_id: str, *, limit: int, cursor: PaginationCursor = None,
    ) -> tuple[list[FilmReview], PaginationCursor]:
        """Получение пагинированного списка рецензий на фильм."""
        ordering = ("_id", DESCENDING)
        filter_query = {"film_id": film_id}
        pagination_query = {"_id": {"$lt": ObjectId(cursor)}}
        results, new_cursor = await self._mongo_repository.get_paginated_results(
            limit=limit, cursor=cursor, cursor_field="id",
            ordering=ordering, filter_query=filter_query, pagination_query=pagination_query,
        )
        return results, new_cursor
