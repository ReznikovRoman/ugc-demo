from typing import Protocol

Message = bytes | str | int | list | dict


class IAsyncRecordMetadata(Protocol):
    """Метаданные сохраненного в очередь сообщения."""

    queue: str
    timestamp: int
