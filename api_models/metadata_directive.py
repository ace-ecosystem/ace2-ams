from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class MetadataDirectiveBase(MetadataBase):
    """Represents a directive that can be applied to an object (observable, alert, event)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the directive")

    value: type_str = Field(description="The value of the directive")


class MetadataDirectiveCreate(MetadataCreate, MetadataDirectiveBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the directive")


class MetadataDirectiveRead(MetadataRead, MetadataDirectiveBase):
    uuid: UUID4 = Field(description="The UUID of the directive")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataDirectiveUpdate(MetadataUpdate, MetadataDirectiveBase):
    value: Optional[type_str] = Field(description="The value of the directive")

    _prevent_none: classmethod = validators.prevent_none("value")
