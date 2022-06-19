import datetime
from typing import Any
from uuid import UUID

from ..types import Model


class FilmBookmark(Model):
    """Фильм, который пользователь сохранил в Закладки."""

    user_id: UUID
    film_id: UUID
    bookmarked: bool
    bookmarked_at: datetime.datetime

    @classmethod
    def from_dict(cls, data: dict) -> "FilmBookmark":
        return cls(
            id=data["id"],
            user_id=data["user_id"], film_id=data["film_id"],
            bookmarked=data["bookmarked"], bookmarked_at=data["bookmarked_at"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id), "film_id": str(self.film_id),
            "bookmarked": self.bookmarked, "bookmarked_at": self.bookmarked_at,
        }
