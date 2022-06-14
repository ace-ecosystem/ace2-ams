from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class MetadataTagBase(MetadataBase):
    """Represents a tag that can be applied to an object (observable, alert, event)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the tag")

    value: type_str = Field(description="The value of the tag")


class MetadataTagCreate(MetadataCreate, MetadataTagBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the tag")


class MetadataTagRead(MetadataRead, MetadataTagBase):
    uuid: UUID4 = Field(description="The UUID of the tag")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataTagUpdate(MetadataUpdate, MetadataTagBase):
    value: Optional[type_str] = Field(description="The value of the tag")

    _prevent_none: classmethod = validators.prevent_none("value")
