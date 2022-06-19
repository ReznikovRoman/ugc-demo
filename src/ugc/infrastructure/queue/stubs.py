import asyncio
import dataclasses
import datetime
import weakref
from typing import Awaitable

from .producers import AsyncProducer
from .typedefs import Message


@dataclasses.dataclass(frozen=True, slots=True)
class InMemoryRecordMetadata:
    queue: str
    timestamp: int = dataclasses.field(default_factory=datetime.datetime.now)


class InMemoryQueue:
    """Очередь, которая хранит все сообщения в памяти."""

    def __init__(self):
        self._queue: asyncio.Queue[Message] = asyncio.Queue()

    async def get(self) -> Message:
        """Чтение сообщения из очереди."""
        return await self._queue.get()

    async def put(self, message: Message) -> None:
        """Сохранение сообщения в очередь."""
        self._queue.put_nowait(message)


class InMemoryProducer(AsyncProducer):
    """Продюсер сообщений в in-memory очередь."""

    def __init__(self, queue: InMemoryQueue):
        self.queue = queue

    async def send(self, queue: str, /, key: str, message: Message) -> Awaitable[InMemoryRecordMetadata]:
        await self.queue.put(message)
        metadata = self._get_metadata(queue)
        _ = weakref.finalize(metadata, metadata.close)
        return metadata

    @staticmethod
    async def _get_metadata(queue: str) -> InMemoryRecordMetadata:
        return InMemoryRecordMetadata(queue)
