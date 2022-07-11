from ..factories import BaseModelFactory
from .types import FilmRating


class FilmRatingFactory(BaseModelFactory[FilmRating]):
    """Фабрика по созданию объектов `FilmRating`."""

    cls = FilmRating

    def create_new(self, **kwargs) -> FilmRating:
        return self.cls(
            user_id=kwargs["user_id"],
            film_id=kwargs["film_id"],
            rating=kwargs["rating"],
        )
