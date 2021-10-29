from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class NodeTagBase(BaseModel):
    """Represents a tag that can be applied to a node (observable instance, analysis, alert, event, user)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the node tag")

    value: type_str = Field(description="The value of the node tag")


class NodeTagCreate(NodeTagBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node tag")


class NodeTagRead(NodeTagBase):
    uuid: UUID4 = Field(description="The UUID of the node tag")

    class Config:
        orm_mode = True


class NodeTagUpdate(NodeTagBase):
    value: Optional[type_str] = Field(description="The value of the node tag")

    _prevent_none: classmethod = validators.prevent_none("value")
