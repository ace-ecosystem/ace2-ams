from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class TagBase(BaseModel):
    """Represents a tag that can be applied objects that accept metadata."""

    value: type_str = Field(description="The value of the tag")


class TagCreate(TagBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the tag")


class TagRead(TagBase):
    uuid: UUID4 = Field(description="The UUID of the tag")

    class Config:
        orm_mode = True


class TagUpdate(TagBase):
    value: Optional[type_str] = Field(description="The value of the tag")

    _prevent_none: classmethod = validators.prevent_none("value")
