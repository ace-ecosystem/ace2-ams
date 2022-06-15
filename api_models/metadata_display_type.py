from pydantic import Field, UUID4
from typing import Optional

from api_models import type_str, validators
from api_models.metadata import MetadataBase, MetadataCreate, MetadataRead, MetadataUpdate


class MetadataDisplayTypeBase(MetadataBase):
    """Represents what should be displayed for the type in the GUI."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the type")

    value: type_str = Field(description="The value of the type")


class MetadataDisplayTypeCreate(MetadataCreate, MetadataDisplayTypeBase):
    pass


class MetadataDisplayTypeRead(MetadataRead, MetadataDisplayTypeBase):
    uuid: UUID4 = Field(description="The UUID of the type")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataDisplayTypeUpdate(MetadataUpdate, MetadataDisplayTypeBase):
    value: Optional[type_str] = Field(description="The value of the type")

    _prevent_none: classmethod = validators.prevent_none("value")
