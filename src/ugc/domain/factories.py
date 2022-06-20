from abc import ABC, abstractmethod
from typing import Type

from .types import BaseModel


class BaseModelFactory(ABC):
    """Базовая фабрика моделей."""

    cls: Type[BaseModel]

    @abstractmethod
    def create_new(self, **kwargs) -> BaseModel:
        """Создание нового объекта."""

    def create_from_serialized(self, data: dict) -> BaseModel:
        """Создание нового объекта из сериализованных данных."""
        return self.cls.from_dict(data)
