from ..factories import BaseModelFactory
from .types import FilmRating


class FilmRatingFactory(BaseModelFactory[FilmRating]):
    """Фабрика по созданию объектов `FilmRating`."""

    cls = FilmRating

    FILM_RATING_RANGE = range(1, 11)

    def create_new(self, **kwargs) -> FilmRating:
        return self.cls(
            user_id=kwargs["user_id"], film_id=kwargs["film_id"],
            rating=self.validate_rating(kwargs["rating"]),
        )

    def validate_rating(self, rating: int) -> int:
        if rating in self.FILM_RATING_RANGE:
            return rating
        raise ValueError(f"Rating must be in range of [1, 10]. Given: {rating}")
