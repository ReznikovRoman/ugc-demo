from typing import Any
from uuid import UUID

from ..types import BaseModel


class FilmReview(BaseModel):
    """Рецензия на фильм."""

    user_id: UUID
    film_id: UUID
    title: str
    review: str

    id: bytes | str | None = None  # noqa: VNE003

    @classmethod
    def from_dict(cls, data: dict) -> "FilmReview":
        dct = {
            "user_id": data["user_id"], "film_id": data["film_id"],
            "title": data["title"], "review": data["review"],
        }
        if review_id := data.get("id"):
            dct["id"] = review_id
        return cls(**dct)

    def to_dict(self) -> dict[str, Any]:
        dct = {
            "user_id": str(self.user_id), "film_id": str(self.film_id),
            "title": self.title, "review": self.review,
        }
        if self.id:
            dct["id"] = str(self.id)
        return dct
