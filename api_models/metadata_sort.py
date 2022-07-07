from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import TypeInt, TypeStr, validators
from api_models.metadata import MetadataRead


class MetadataSortCreate(BaseModel):
    description: Optional[TypeStr] = Field(description="An optional human-readable description of the sort")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the sort")

    value: TypeInt = Field(description="The value of the sort")


class MetadataSortRead(MetadataRead):
    description: Optional[TypeStr] = Field(description="An optional human-readable description of the sort")

    uuid: UUID4 = Field(description="The UUID of the sort")

    value: TypeInt = Field(description="The value of the sort")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.value)


class MetadataSortUpdate(BaseModel):
    description: Optional[TypeStr] = Field(description="An optional human-readable description of the sort")

    value: Optional[TypeInt] = Field(description="The value of the sort")

    _prevent_none: classmethod = validators.prevent_none("value")
