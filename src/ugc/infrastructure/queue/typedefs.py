from typing import Protocol

Message = bytes | str | int | list | dict


class IAsyncRecordMetadata(Protocol):
    """Метаданные сохраненного в очередь сообщения."""

    queue: str
    timestamp: int


class IConsumerRecord(Protocol):
    """Сообщение из очереди."""

    key: str
    value: Message
