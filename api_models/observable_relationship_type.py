from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class ObservableRelationshipTypeBase(BaseModel):
    """Represents a relationship type that can be used in a relationship applied to an observable."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the relationship type"
    )

    value: type_str = Field(description="The value of the relationship type")


class ObservableRelationshipTypeCreate(ObservableRelationshipTypeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the relationship type")


class ObservableRelationshipTypeRead(ObservableRelationshipTypeBase):
    uuid: UUID4 = Field(description="The UUID of the relationship type")

    class Config:
        orm_mode = True


class ObservableRelationshipTypeUpdate(ObservableRelationshipTypeBase):
    value: Optional[type_str] = Field(description="The value of the relationship type")

    _prevent_none: classmethod = validators.prevent_none("value")
