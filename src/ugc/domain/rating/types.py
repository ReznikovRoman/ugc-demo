from typing import Any
from uuid import UUID

from ..types import BaseModel


class FilmRating(BaseModel):
    """Оценки фильма."""

    user_id: UUID
    film_id: UUID
    rating: int

    @classmethod
    def from_dict(cls, data: dict) -> "FilmRating":
        return cls(user_id=data["user_id"], film_id=data["film_id"], rating=data["rating"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": str(self.user_id),
            "film_id": str(self.film_id),
            "rating": self.rating,
        }
