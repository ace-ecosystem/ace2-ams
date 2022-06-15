from pydantic import Field, UUID4
from typing import Optional

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class MetadataDisplayValueBase(MetadataBase):
    """Represents what should be displayed for the value in the GUI."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the value")

    value: type_str = Field(description="The value")


class MetadataDisplayValueCreate(MetadataCreate, MetadataDisplayValueBase):
    pass


class MetadataDisplayValueRead(MetadataRead, MetadataDisplayValueBase):
    uuid: UUID4 = Field(description="The UUID of the value")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataDisplayValueUpdate(MetadataUpdate, MetadataDisplayValueBase):
    value: Optional[type_str] = Field(description="The value")

    _prevent_none: classmethod = validators.prevent_none("value")
