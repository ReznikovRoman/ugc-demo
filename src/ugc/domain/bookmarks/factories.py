import datetime

from ..factories import BaseModelFactory
from .types import FilmBookmark


class FilmBookmarkFactory(BaseModelFactory[FilmBookmark]):
    """Фабрика по созданию объектов `FilmBookmark`."""

    cls = FilmBookmark

    def create_new(self, **kwargs) -> FilmBookmark:
        return self.cls(
            user_id=kwargs["user_id"], film_id=kwargs["film_id"],
            bookmarked=kwargs["bookmarked"], bookmarked_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
