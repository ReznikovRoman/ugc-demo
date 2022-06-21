import asyncio
import dataclasses
from typing import Awaitable, Callable, List

from ugc.infrastructure.queue.consumers import AsyncConsumer
from ugc.infrastructure.queue.typedefs import IConsumerRecord


@dataclasses.dataclass
class ProcessorService:
    """Обработчик сообщений из очереди."""

    consumer: AsyncConsumer
    concurrency: int
    message_callback: Callable[[IConsumerRecord], Awaitable[None]]

    _tasks: List[asyncio.Task[None]] = dataclasses.field(default_factory=list)

    def start_processing(self) -> None:
        """Запуск обработки сообщений.

        Используем `concurrency` для создания нескольких обработчиков.
        """
        self._tasks = [
            asyncio.create_task(self._processor_loop())
            for _ in range(int(self.concurrency))
        ]

    def stop_processing(self) -> None:
        """Остановка всех обработчиков."""
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()

    async def process_event(self) -> None:
        """Обработка сообщения из очереди."""
        message = await self.consumer.fetch_message()
        await self.message_callback(message)

    async def _processor_loop(self) -> None:
        while True:
            await self.process_event()
