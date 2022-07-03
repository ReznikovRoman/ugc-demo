from aredis_om import NotFoundError as RedisNotFoundError

from ugc.common.exceptions import NotFoundError
from ugc.infrastructure.db.repositories import BaseRedisRepository

from .factories import FilmProgressFactory
from .models import UserFilmProgress
from .types import FilmProgress


class FilmProgressRepository(BaseRedisRepository[UserFilmProgress]):
    """Репозиторий для работы с данными прогресса фильма."""

    model = UserFilmProgress

    def __init__(self, progress_factory: FilmProgressFactory) -> None:
        assert isinstance(progress_factory, FilmProgressFactory)
        self._factory = progress_factory

    async def get_by_film_id(self, *, user_id: str, film_id: str) -> FilmProgress:
        """Получение прогресса фильма для пользователя по `film_id`."""
        try:
            obj = await self.model.find(
                (self.model.user_id == user_id) &
                (self.model.film_id == film_id),
            ).first()
            data = obj.dict()
            data["id"] = data.pop("pk")
            return self._factory.create_from_serialized(data)
        except RedisNotFoundError:
            raise NotFoundError()

    async def update_or_create_progress(self, progress: FilmProgress, /) -> FilmProgress:
        """Создание или обновление прогресса фильма.

        Если объект прогресса уже есть в БД, то обновляем `viewed_frame` для него.
        Если объекта еще нет - создаем новый.
        """
        await self.update_or_create(
            defaults={"viewed_frame": progress.viewed_frame},
            user_id=str(progress.user_id),
            film_id=str(progress.film_id),
        )
        return progress
