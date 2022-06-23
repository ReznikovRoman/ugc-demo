from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from .types import BaseModel

_BM = TypeVar("_BM", bound=BaseModel)


class BaseModelFactory(ABC, Generic[_BM]):
    """Базовая фабрика моделей."""

    cls: Type[_BM]

    @abstractmethod
    def create_new(self, **kwargs) -> _BM:
        """Создание нового объекта."""

    def create_from_serialized(self, data: dict) -> _BM:
        """Создание нового объекта из сериализованных данных."""
        return self.cls.from_dict(data)
