from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class NodeDirectiveBase(BaseModel):
    """Represents a node directive that can be applied to a node (typically an observable)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the node directive")

    value: type_str = Field(description="The value of the node directive")


class NodeDirectiveCreate(NodeDirectiveBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node directive")


class NodeDirectiveRead(NodeDirectiveBase):
    uuid: UUID4 = Field(description="The UUID of the node directive")

    class Config:
        orm_mode = True


class NodeDirectiveUpdate(NodeDirectiveBase):
    value: Optional[type_str] = Field(description="The value of the node directive")

    _prevent_none: classmethod = validators.prevent_none("value")
