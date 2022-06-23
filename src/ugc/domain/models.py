from abc import ABC

from aredis_om import HashModel

from ugc.core.config import get_settings

settings = get_settings()


class BaseHashModel(HashModel, ABC):
    """Базовая модель типа `HashModel` сервиса."""

    class Meta:
        global_key_prefix = settings.REDIS_KEY_PREFIX
