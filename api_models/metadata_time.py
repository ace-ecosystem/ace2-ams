from datetime import datetime
from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class MetadataTimeBase(MetadataBase):
    """Represents a time that can be applied to an object (observable, alert, event)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the time")

    value: datetime = Field(description="The value of the time")


class MetadataTimeCreate(MetadataCreate, MetadataTimeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the time")


class MetadataTimeRead(MetadataRead, MetadataTimeBase):
    uuid: UUID4 = Field(description="The UUID of the time")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataTimeUpdate(MetadataUpdate, MetadataTimeBase):
    value: Optional[datetime] = Field(description="The value of the time")

    _prevent_none: classmethod = validators.prevent_none("value")
