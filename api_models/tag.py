from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class TagBase(MetadataBase):
    """Represents a tag that can be applied to an object (observable, alert, event)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the tag")

    value: type_str = Field(description="The value of the tag")


class TagCreate(MetadataCreate, TagBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the tag")


class TagRead(MetadataRead, TagBase):
    uuid: UUID4 = Field(description="The UUID of the tag")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class TagUpdate(MetadataUpdate, TagBase):
    value: Optional[type_str] = Field(description="The value of the tag")

    _prevent_none: classmethod = validators.prevent_none("value")
