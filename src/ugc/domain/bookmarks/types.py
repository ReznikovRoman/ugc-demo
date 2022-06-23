import datetime
from typing import Any
from uuid import UUID

from ulid import ULID

from ..types import BaseModel


class FilmBookmark(BaseModel):
    """Фильм, который пользователь сохранил в закладки."""

    user_id: UUID
    film_id: UUID
    bookmarked: bool
    bookmarked_at: datetime.datetime

    id: ULID | str | None = None  # noqa: VNE003

    @classmethod
    def from_dict(cls, data: dict) -> "FilmBookmark":
        dct = {
            "user_id": data["user_id"],
            "film_id": data["film_id"],
            "bookmarked": bool(data["bookmarked"]),
            "bookmarked_at": data["bookmarked_at"],
        }
        if bookmark_id := data.get("id"):
            dct["id"] = bookmark_id
        return cls(**dct)

    def to_dict(self) -> dict[str, Any]:
        dct = {
            "user_id": str(self.user_id), "film_id": str(self.film_id),
            "bookmarked": self.bookmarked, "bookmarked_at": self.bookmarked_at,
        }
        if self.id:
            dct["id"] = str(self.id)
        return dct
