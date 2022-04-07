"""
Environment variables / configuration
"""

import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    Reads OS environment variables and maps them into attributes using Pydantic
    """

    cookies_samesite: str = Field(default="lax")
    cookies_secure: bool = Field(default=True)
    database_api_url: str
    jwt_access_expire_seconds: int
    jwt_algorithm: str
    jwt_refresh_expire_seconds: int
    jwt_secret: str


def get_settings():
    """
    Helper function to read the settings. Can be patched for unit testing.
    """

    return Settings()
