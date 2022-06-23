import logging
from abc import ABC, abstractmethod
from typing import AsyncIterator, Awaitable, Callable

from aiokafka.errors import KafkaError
from aiokafka.producer import AIOKafkaProducer
from aiokafka.structs import RecordMetadata

from .typedefs import IAsyncRecordMetadata, Message


class AsyncProducer(ABC):
    """Асинхронный продюсер сообщений в очередь."""

    @abstractmethod
    async def send(self, queue: str, /, key: str, message: Message) -> Awaitable[IAsyncRecordMetadata]:
        """Отправка сообщения `message` с ключом роутинга `key` в очередь `queue`."""


class KafkaProducer(AsyncProducer):
    """Продюсер сообщений с использованием Kafka."""

    def __init__(self, client: AIOKafkaProducer) -> None:
        assert isinstance(client, AIOKafkaProducer)
        self._client = client

    async def send(self, queue: str, /, key: str, message: Message) -> Awaitable[RecordMetadata]:
        try:
            return await self._client.send(queue, key=key, value=message)
        except KafkaError as e:
            logging.error(e)


async def init_kafka_producer_client(
    servers: list[str],
    key_serializer: Callable[[str], bytes],
    value_serializer: Callable[[Message], bytes],
) -> AsyncIterator[AIOKafkaProducer]:
    assert isinstance(servers, list), "`servers` is not an instance of `list`"
    assert isinstance(servers[0], str), "`servers` must be a list of strings"
    assert callable(key_serializer), "`key_serializer` is not callable"
    assert callable(value_serializer), "`value_serializer` is not callable"

    producer = AIOKafkaProducer(
        bootstrap_servers=servers,
        key_serializer=key_serializer,
        value_serializer=value_serializer,
    )
    await producer.start()
    yield producer
    await producer.stop()
