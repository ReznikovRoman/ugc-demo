from typing import Any
from uuid import UUID

from ugc.helpers import delay_tasks
from ugc.infrastructure.queue.producers import AsyncProducer

from .factories import FilmBookmarkFactory
from .types import FilmBookmark


class BookmarkDispatcherService:
    """Сервис для диспатчинга событий об изменениях в закладках.

    В текущей реализации события о добавлении и удалении закладок попадают в одну очередь.
    """

    def __init__(self, bookmark_factory: FilmBookmarkFactory, producer: AsyncProducer, config: dict[str, Any]) -> None:
        assert isinstance(bookmark_factory, FilmBookmarkFactory)
        self._bookmark_factory = bookmark_factory

        assert isinstance(producer, AsyncProducer)
        self._producer = producer

        assert isinstance(config, dict)
        self._config = config

    async def dispatch_bookmark_switch(self, *, user_id: UUID, film_id: UUID, bookmarked: bool) -> FilmBookmark:
        bookmark = self._bookmark_factory.create_new(user_id=user_id, film_id=film_id, bookmarked=bookmarked)
        delay_tasks(
            self._producer.send(
                self._config["QUEUE_BOOKMARKS_NAME"], key=f"{user_id}:{film_id}", message=bookmark.to_dict(),
            ),
        )
        return bookmark
