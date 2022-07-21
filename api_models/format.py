from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class FormatBase(BaseModel):
    """Represents a format used to inform a GUI how an item is intended to be displayed."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the format")

    value: type_str = Field(description="The value of the format")


class FormatCreate(FormatBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the format")


class FormatRead(FormatBase):
    uuid: UUID4 = Field(description="The UUID of the format")

    class Config:
        orm_mode = True


class FormatUpdate(FormatBase):
    value: Optional[type_str] = Field(description="The value of the format")

    _prevent_none: classmethod = validators.prevent_none("value")
