from ..factories import BaseModelFactory
from .types import FilmProgress


class FilmProgressFactory(BaseModelFactory[FilmProgress]):
    """Фабрика по созданию объектов `FilmProgress`."""

    cls = FilmProgress

    def create_new(self, **kwargs) -> FilmProgress:
        return self.cls(
            user_id=kwargs["user_id"],
            film_id=kwargs["film_id"],
            viewed_frame=kwargs["viewed_frame"],
        )
