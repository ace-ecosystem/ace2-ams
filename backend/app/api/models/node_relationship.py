from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class NodeRelationshipBase(BaseModel):
    """Represents a node relationship that can be applied to a node (typically an observable)."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node relationship"
    )

    value: type_str = Field(description="The value of the node relationship")


class NodeRelationshipCreate(NodeRelationshipBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node relationship")


class NodeRelationshipRead(NodeRelationshipBase):
    uuid: UUID4 = Field(description="The UUID of the node relationship")

    class Config:
        orm_mode = True


class NodeRelationshipUpdate(NodeRelationshipBase):
    value: Optional[type_str] = Field(description="The value of the node relationship")

    _prevent_none: classmethod = validators.prevent_none("value")
