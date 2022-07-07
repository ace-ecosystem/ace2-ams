from pydantic import BaseModel, Field, UUID4
from uuid import uuid4

from api_models import TypeStr


class MetadataBase(BaseModel):
    """Represents an individual metadata object."""

    pass


class MetadataCreate(MetadataBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the metadata")


class MetadataRead(MetadataBase):

    metadata_type: TypeStr = Field(description="The type of the metadata")

    uuid: UUID4 = Field(description="The UUID of the metadata")

    class Config:
        orm_mode = True


class MetadataUpdate(MetadataBase):
    pass
