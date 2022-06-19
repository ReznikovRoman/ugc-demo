from typing import Any
from uuid import UUID

from ..types import BaseModel


class FilmProgress(BaseModel):
    """Прогресс просмотра фильма."""

    user_id: UUID
    film_id: UUID
    viewed_frame: int

    @classmethod
    def from_dict(cls, data: dict) -> "FilmProgress":
        return cls(user_id=data["user_id"], film_id=data["film_id"], viewed_frame=data["viewed_frame"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": str(self.user_id),
            "film_id": str(self.film_id),
            "viewed_frame": self.viewed_frame,
        }
