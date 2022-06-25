from functools import lru_cache

from pydantic import BaseSettings, Field


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

    # Netflix Auth
    NETFLIX_AUTH_BASE_URL: str = Field(env="TEST_NETFLIX_AUTH_BASE_URL")

    class Config(EnvConfig):
        env_prefix = "NUGC_"
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings() -> "Test":
    return Test()
