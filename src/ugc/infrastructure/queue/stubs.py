import asyncio
import dataclasses
import datetime
import weakref
from typing import Awaitable

from .consumers import AsyncConsumer
from .producers import AsyncProducer
from .typedefs import Message


@dataclasses.dataclass(frozen=True, slots=True)
class InMemoryRecordMetadata:
    queue: str
    timestamp: int = dataclasses.field(default_factory=datetime.datetime.now)


@dataclasses.dataclass(frozen=True, slots=True)
class InMemoryConsumerRecord:
    key: str
    value: Message


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


class InMemoryProcessor(AsyncProducer, AsyncConsumer):
    """Обработчик сообщений из in-memory очереди."""

    def __init__(self, queue: InMemoryQueue):
        self.queue = queue

    async def send(self, queue: str, /, key: str, message: Message) -> Awaitable[InMemoryRecordMetadata]:
        await self.queue.put(message)
        metadata = self._get_metadata(queue)
        _ = weakref.finalize(metadata, metadata.close)
        return metadata

    async def fetch_message(self) -> InMemoryConsumerRecord:
        message = await self.queue.get()
        return InMemoryConsumerRecord(key="inmemory", value=message)

    @staticmethod
    async def _get_metadata(queue: str) -> InMemoryRecordMetadata:
        return InMemoryRecordMetadata(queue)
