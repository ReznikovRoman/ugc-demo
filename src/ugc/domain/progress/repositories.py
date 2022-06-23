from ugc.infrastructure.db.repositories import BaseRepository

from .models import UserFilmProgress
from .types import FilmProgress


class FilmProgressRepository(BaseRepository[UserFilmProgress]):
    """Репозиторий для работы с данными прогресса фильма."""

    model = UserFilmProgress

    async def track_progress(self, progress: FilmProgress, /) -> FilmProgress:
        """Трекинг прогресса фильма.

        Если объект прогресса уже есть в БД, то обновляем `viewed_frame` для него.
        Если объекта еще нет - создаем новый.
        """
        obj, _ = await self.update_or_create(
            defaults={"viewed_frame": progress.viewed_frame},
            user_id=str(progress.user_id),
            film_id=str(progress.film_id),
        )
        return progress
