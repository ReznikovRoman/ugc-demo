from ...common.exceptions import NotFoundError
from .repositories import BookmarkRepository
from .types import FilmBookmark


class BookmarkService:
    """Сервис для работы с закладками."""

    def __init__(self, bookmark_repository: BookmarkRepository) -> None:
        assert isinstance(bookmark_repository, BookmarkRepository)
        self._repository = bookmark_repository

    async def handle_bookmark(self, bookmark: FilmBookmark, /) -> FilmBookmark:
        """Обработка 'закладки' фильма."""
        user_id, film_id = self._prepare_ids(bookmark)
        try:
            return await self._repository.get_by_film_id(user_id=user_id, film_id=film_id)
        except NotFoundError:
            return await self._repository.create(bookmark)

    async def delete_by_film_id(self, bookmark: FilmBookmark, /) -> None:
        """Удаление закладки пользователя по id фильма."""
        user_id, film_id = self._prepare_ids(bookmark)
        await self._repository.delete(user_id=user_id, film_id=film_id)

    @staticmethod
    def _prepare_ids(bookmark: FilmBookmark) -> tuple[str, str]:
        user_id = str(bookmark.user_id)
        film_id = str(bookmark.film_id)
        return user_id, film_id
