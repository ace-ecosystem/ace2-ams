from pydantic import BaseModel
from typing import Optional

from api.models import type_str


class Auth(BaseModel):
    """Represents the response to successful authentication."""

    access_token: type_str

    refresh_token: Optional[type_str]

    token_type: type_str
