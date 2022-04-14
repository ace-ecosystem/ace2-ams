from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class NodeRelationshipTypeBase(BaseModel):
    """Represents a node relationship type that can be used in a relationship applied to a node (typically an observable)."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node relationship type"
    )

    value: type_str = Field(description="The value of the node relationship type")


class NodeRelationshipTypeCreate(NodeRelationshipTypeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node relationship type")


class NodeRelationshipTypeRead(NodeRelationshipTypeBase):
    uuid: UUID4 = Field(description="The UUID of the node relationship type")

    class Config:
        orm_mode = True


class NodeRelationshipTypeUpdate(NodeRelationshipTypeBase):
    value: Optional[type_str] = Field(description="The value of the node relationship type")

    _prevent_none: classmethod = validators.prevent_none("value")
