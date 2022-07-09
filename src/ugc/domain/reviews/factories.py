from ..factories import BaseModelFactory
from .types import FilmReview


class FilmReviewFactory(BaseModelFactory[FilmReview]):
    """Фабрика по созданию объектов `FilmReview`."""

    cls = FilmReview

    def create_new(self, **kwargs) -> FilmReview:
        return self.cls(
            user_id=kwargs["user_id"], film_id=kwargs["film_id"],
            title=kwargs["title"], review=kwargs["review"],
        )
