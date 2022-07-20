from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class MetadataCriticalPointBase(MetadataBase):
    """Represents a critical point that can be applied to an object (observable, alert, event)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the critical point")

    value: type_str = Field(description="The 'value' of the critical point potentially the 'type' of critical point (e.g. 'tag', 'detection_point')")


class MetadataCriticalPointCreate(MetadataCreate, MetadataCriticalPointBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the critical point")


class MetadataCriticalPointRead(MetadataRead, MetadataCriticalPointBase):
    uuid: UUID4 = Field(description="The UUID of the critical point")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataCriticalPointUpdate(MetadataUpdate, MetadataCriticalPointBase):
    value: Optional[type_str] = Field(description="The value of the critical point")

    _prevent_none: classmethod = validators.prevent_none("value")
