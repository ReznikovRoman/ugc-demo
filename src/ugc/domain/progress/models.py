from uuid import UUID

from aredis_om import Field

from ugc.domain.models import BaseHashModel


class UserFilmProgress(BaseHashModel):
    """Прогресс просмотра фильма для пользователя."""

    user_id: UUID = Field(index=True)
    film_id: UUID = Field(index=True)
    viewed_frame: int
