from functools import lru_cache

from pydantic import BaseSettings, Field, validator


class EnvConfig(BaseSettings.Config):

    @classmethod
    def prepare_field(cls, field) -> None:
        if "env_names" in field.field_info.extra:
            return
        return super().prepare_field(field)


class Test(BaseSettings):
    """Настройки для функциональных тестов."""

    # Tests
    CLIENT_BASE_URL: str = Field(env="TEST_CLIENT_BASE_URL")
    SERVER_BASE_URL: str = Field(env="TEST_SERVER_BASE_URL")

    # Redis
    REDIS_OM_URL: str

    # MongoDB
    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_NAME: str
    MONGODB_HOST: str
    MONGODB_PORT: int
    MONGODB_URL: str | None = Field(None)

    # Netflix Auth
    NETFLIX_AUTH_BASE_URL: str = Field(env="TEST_NETFLIX_AUTH_BASE_URL")

    class Config(EnvConfig):
        env_prefix = "NUGC_"
        case_sensitive = True
        env_file = ".env"

    @validator("MONGODB_URL", pre=True)
    def get_mongodb_url(cls, value, values) -> str:  # noqa: N805
        if value is not None:
            return value
        user = values["MONGODB_USER"]
        password = values["MONGODB_PASSWORD"]
        host = values["MONGODB_HOST"]
        port = values["MONGODB_PORT"]
        database = values["MONGODB_NAME"]
        return f"mongodb://{user}:{password}@{host}:{port}/{database}?authSource=admin"


@lru_cache()
def get_settings() -> "Test":
    return Test()
