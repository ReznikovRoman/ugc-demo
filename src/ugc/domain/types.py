import abc
import dataclasses
from abc import ABC, abstractmethod
from typing import Any

Id = int


class _ModelMeta(type):
    """Мета-класс для создания датаклассов."""

    _dataclass_options = {
        "init": True,
        "repr": True,
        "eq": True,
        "order": True,
        "unsafe_hash": True,
        "frozen": True,
        "kw_only": True,
        "match_args": True,
        "slots": True,
    }
    _convert_to_dataclass = dataclasses.dataclass(**_dataclass_options)

    def __new__(cls, name, bases, namespace):  # noqa: N805
        obj = super().__new__(cls, name, bases, namespace)
        if "__slots__" in namespace:
            # Пересоздание класса внутри dataclasses.dataclass
            return obj
        return cls._convert_to_dataclass(obj)


class _AbstractModelMeta(_ModelMeta, abc.ABCMeta):
    ...


class BaseModel(metaclass=_AbstractModelMeta):
    """Базовый класс модели для тех сущностей, у которых нет поля `id`.

    Для остальных случаев следует использовать `Model`.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "BaseModel":
        """Создание объекта из сериализованных данных `data`."""

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Сериализация объекта."""


class Model(BaseModel, ABC):
    """Базовый класс модели.

    Модели по сути являются датаклассами, но не требуют соответствующего декоратора.
    Модели/инстансы моделей могут быть проверены стандартными `issubclass()`/`isinstance()`.

    Инстансы моделей иммутабельны.
    """

    id: Id  # noqa: VNE003
