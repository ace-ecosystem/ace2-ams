from pydantic import BaseModel, Field


class Auth(BaseModel):
    """Represents the necessary data to authenticate a username/password."""

    new_refresh_token: str = Field(
        description="The new refresh token to assign to the user if the authentication is successful"
    )

    password: str = Field(description="The password to use for authentication")

    username: str = Field(description="The username to use for authentication")


class ValidateRefreshToken(BaseModel):
    """Represents the necessary data for the database API to validate the given refresh token."""

    username: str

    refresh_token: str

    new_refresh_token: str
