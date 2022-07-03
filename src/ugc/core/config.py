from functools import lru_cache
from typing import Literal, Union

from pydantic import AnyHttpUrl, Field, validator
from pydantic.env_settings import BaseSettings


class EnvConfig(BaseSettings.Config):

    @classmethod
    def prepare_field(cls, field) -> None:
        if "env_names" in field.field_info.extra:
            return
        return super().prepare_field(field)


class Settings(BaseSettings):
    """Настройки проекта."""

    # Project
    PROJECT_BASE_URL: str
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str | None = Field(None, env="NAA_SERVER_NAME")
    SERVER_HOSTS: Union[str, list[AnyHttpUrl]]
    PROJECT_NAME: str
    DEBUG: bool = Field(False)

    # Auth
    JWT_AUTH_SECRET_KEY: str = Field(env="NAA_SECRET_KEY")
    JWT_AUTH_ALGORITHM: str = "HS256"

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_MAIN_DB: int
    REDIS_OM_URL: str
    REDIS_DEFAULT_CHARSET: str = "utf-8"
    REDIS_DECODE_RESPONSES: bool | Literal[True, False] = True
    REDIS_RETRY_ON_TIMEOUT: bool = True
    REDIS_KEY_PREFIX: str = Field("ugc")

    # Redis
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_NAME: str
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_URL: str | None = Field(None)

    # Queue
    QUEUE_PROGRESS_NAME: str = Field("progress-topic")
    QUEUE_PROGRESS_GROUP: str = Field("progress-group")
    QUEUE_PROGRESS_CONSUMERS: int = Field(2)
    QUEUE_BOOKMARKS_NAME: str = Field("bookmarks-topic")
    QUEUE_BOOKMARKS_GROUP: str = Field("bookmarks-group")
    QUEUE_BOOKMARKS_CONSUMERS: int = Field(2)
    QUEUE_ENABLE_AUTOCOMMIT: bool = Field(True)
    QUEUE_AUTO_COMMIT_INTERVAL_MS: int = Field(1000)
    QUEUE_AUTO_OFFSET_RESET: str = Field("earliest")

    # Kafka
    KAFKA_URL: str

    # Config
    USE_STUBS: bool = Field(False)
    TESTING: bool = Field(False)
    CI: bool = Field(False)

    class Config(EnvConfig):
        env_prefix = "NUGC_"
        case_sensitive = True

    @validator("SERVER_HOSTS", pre=True)
    def _assemble_server_hosts(cls, server_hosts):
        if isinstance(server_hosts, str):
            return [item.strip() for item in server_hosts.split(",")]
        return server_hosts

    @validator("MONGODB_URL", pre=True)
    def get_mongodb_url(cls, value, values) -> str:
        if value is not None:
            return value
        user = values["MONGODB_USER"]
        password = values["MONGODB_PASSWORD"]
        host = values["MONGODB_HOST"]
        port = values["MONGODB_PORT"]
        database = values["MONGODB_NAME"]
        return f"mongodb://{user}:{password}@{host}:{port}/{database}"


@lru_cache()
def get_settings() -> "Settings":
    return Settings()
