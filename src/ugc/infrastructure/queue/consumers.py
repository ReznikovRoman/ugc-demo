from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Callable

from aiokafka.consumer import AIOKafkaConsumer
from aiokafka.errors import ConsumerStoppedError
from aiokafka.structs import ConsumerRecord

from .typedefs import IConsumerRecord, Message


class AsyncConsumer(ABC):
    """Асинхронный консьюмер сообщений из очереди."""

    queue: str

    @abstractmethod
    async def fetch_message(self) -> IConsumerRecord:
        """Чтение сообщения из очереди."""


class KafkaConsumer(AsyncConsumer):
    """Консьюмер сообщений из Kafka."""

    def __init__(self, client: AIOKafkaConsumer):
        assert isinstance(client, AIOKafkaConsumer)
        self._client = client

    async def fetch_message(self) -> ConsumerRecord:
        assert self._client._closed is False, "Consumer is closed"
        try:
            return await self._client.getone()
        except ConsumerStoppedError:
            raise StopAsyncIteration


async def init_kafka_consumer_client(
    config: dict[str, Any],
    topic: str,
    key_deserializer: Callable[[bytes], str],
    value_deserializer: Callable[[bytes], Message],
    group_id: str,
) -> AsyncIterator[AIOKafkaConsumer]:
    assert isinstance(topic, str), "`topic` must be a string"
    assert callable(key_deserializer), "`key_deserializer` is not callable"
    assert callable(value_deserializer), "`value_deserializer` is not callable"
    assert isinstance(group_id, str), "`group_id` must be a string"

    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=config["KAFKA_URL"],
        key_deserializer=key_deserializer,
        value_deserializer=value_deserializer,
        group_id=group_id,
        enable_auto_commit=config["QUEUE_ENABLE_AUTOCOMMIT"],
        auto_commit_interval_ms=config["QUEUE_AUTO_COMMIT_INTERVAL_MS"],
        auto_offset_reset=config["QUEUE_AUTO_OFFSET_RESET"],
    )
    await consumer.start()
    yield consumer
    await consumer.stop()
