from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class MetadataDetectionPointBase(MetadataBase):
    """Represents a detection point that can be applied to an object (observable, alert, event)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the detection point")

    value: type_str = Field(description="The value of the detection point")


class MetadataDetectionPointCreate(MetadataCreate, MetadataDetectionPointBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the detection point")


class MetadataDetectionPointRead(MetadataRead, MetadataDetectionPointBase):
    uuid: UUID4 = Field(description="The UUID of the detection point")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataDetectionPointUpdate(MetadataUpdate, MetadataDetectionPointBase):
    value: Optional[type_str] = Field(description="The value of the detection point")

    _prevent_none: classmethod = validators.prevent_none("value")
