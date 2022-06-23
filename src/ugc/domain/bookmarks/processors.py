from ugc.infrastructure.queue.typedefs import IConsumerRecord

from .factories import FilmBookmarkFactory
from .services import BookmarkService


class BookmarkProcessor:
    """Обработка сообщений о закладках."""

    def __init__(self, bookmark_factory: FilmBookmarkFactory, bookmark_service: BookmarkService):
        assert isinstance(bookmark_factory, FilmBookmarkFactory)
        self._factory = bookmark_factory

        assert isinstance(bookmark_service, BookmarkService)
        self._service = bookmark_service

    async def __call__(self, message: IConsumerRecord) -> bool:
        bookmark = self._factory.create_from_serialized(message.value)
        if bookmark.bookmarked:
            await self._service.handle_bookmark(bookmark)
            return True
        await self._service.delete_by_film_id(bookmark)
        return False
