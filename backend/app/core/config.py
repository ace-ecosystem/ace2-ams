"""
Environment variables / configuration
"""

from typing import List, Union

from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    """
    Reads OS environment variables and maps them into attributes using Pydantic
    """

    cookies_samesite: str = Field(default="lax")
    cookies_secure: bool = Field(default=True)
    cors_origins: Union[str, List[str]]
    database_url: PostgresDsn
    jwt_access_expire_seconds: int
    jwt_algorithm: str
    jwt_refresh_expire_seconds: int
    jwt_secret: str

    # Pydantic has a limitation around supporting comma separated lists in the environment variables
    # https://github.com/samuelcolvin/pydantic/issues/1458
    @validator("cors_origins", pre=True)
    def _validate_cors_origins(cls, value):  # pylint: disable=no-self-argument,no-self-use
        return [item.strip() for item in value.split(",")]


def get_settings():
    """
    Helper function to read the settings. Can be patched for unit testing.
    """

    return Settings()
