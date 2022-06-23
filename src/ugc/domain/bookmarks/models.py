import datetime
from uuid import UUID

from aredis_om import Field

from ugc.domain.models import BaseHashModel


class FilmBookmark(BaseHashModel):
    """Фильм, находящийся в закладках у пользователя."""

    user_id: UUID = Field(index=True)
    film_id: UUID = Field(index=True)
    bookmarked_at: datetime.datetime
