from uuid import UUID

from aredis_om import Field

from ugc.domain.models import BaseHashModel


class FilmRating(BaseHashModel):
    """Рейтинг фильма, поставленный пользователем."""

    user_id: UUID = Field(index=True)
    film_id: UUID = Field(index=True)
    rating: int
