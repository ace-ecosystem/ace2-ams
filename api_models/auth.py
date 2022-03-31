from pydantic import BaseModel, Field
from typing import Optional

from api_models import type_str
from api_models.user import UserRead


class Auth(BaseModel):
    """Represents the necessary data to authenticate a username/password."""

    new_refresh_token: str = Field(
        description="The new refresh token to assign to the user if the authentication is successful"
    )

    password: str = Field(description="The password to use for authentication")

    username: str = Field(description="The username to use for authentication")


class AuthResponse(BaseModel):
    """Represents the response to successful authentication."""

    access_token: type_str

    refresh_token: Optional[type_str]

    token_type: type_str


class ValidateRefreshToken(BaseModel):
    """Represents the necessary data for the database API to validate the given refresh token."""

    username: str

    refresh_token: str

    new_refresh_token: str
