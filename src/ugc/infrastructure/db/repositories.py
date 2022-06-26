import functools
from operator import and_
from typing import Generic, NamedTuple, Type, TypeVar

from aredis_om.model.model import NotFoundError, RedisModel

from ugc.helpers import resolve_callables

_RM = TypeVar("_RM", bound=RedisModel)


class ModelInfo(NamedTuple):
    model: _RM
    created: bool


class BaseRepository(Generic[_RM]):
    """Базовый репозиторий для работы с данными модели `RedisModel`."""

    model: Type[_RM]

    async def get_or_create(self, defaults: dict | None = None, **kwargs) -> ModelInfo:
        """Получение объекта по `expressions`, создание нового при необходимости.

        Args:
            defaults: словарь с парами ключ-значение, который будет использоваться при создании объекта.
            **kwargs: поля для поиска.

        Returns:
            Кортеж с объектом и булевой переменной, показывающей был ли создан новый объект.
        """
        query = self._get_equal_query(**kwargs)
        try:
            obj = await self.model.find(query).first()
            return ModelInfo(obj, False)
        except NotFoundError:
            params = dict(resolve_callables(self._extract_model_params(defaults, **kwargs)))
            obj = self.model(**params)
            await obj.save()
            return ModelInfo(obj, True)

    async def update_or_create(self, defaults: dict | None = None, **kwargs) -> ModelInfo:
        """Поиск объекта по заданным `kwargs` и обновление полей в соответствии с `defaults`.

        Если объект не был найден по `kwargs`, то будет создан новый.

        Args:
            defaults: словарь с парами ключ-значение, который будет использоваться при обновлении объекта.
            **kwargs: поля для поиска.

        Returns:
            Кортеж с объектом и булевой переменной, показывающей был ли создан новый объект.
        """
        defaults = defaults or {}
        obj, created = await self.get_or_create(defaults, **kwargs)
        if created:
            return ModelInfo(obj, created)
        for key, value in resolve_callables(defaults):
            setattr(obj, key, value)
        await obj.save()
        return ModelInfo(obj, False)

    def _get_equal_query(self, **kwargs) -> bool:
        expressions = (
            getattr(self.model, field) == value
            for field, value in kwargs.items()
        )
        query = functools.reduce(and_, expressions)
        return query

    @staticmethod
    def _extract_model_params(defaults: dict | None, **kwargs) -> dict:
        defaults = defaults or {}
        params = {k: v for k, v in kwargs.items()}
        params.update(defaults)
        return params
