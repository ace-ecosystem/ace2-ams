from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class NodeHistoryActionBase(BaseModel):
    """Represents a historical action that can be performed on a node."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node history action"
    )

    value: type_str = Field(description="The value of the node history action")


class NodeHistoryActionCreate(NodeHistoryActionBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node history action")


class NodeHistoryActionRead(NodeHistoryActionBase):
    uuid: UUID4 = Field(description="The UUID of the node history action")

    class Config:
        orm_mode = True


class NodeHistoryActionUpdate(NodeHistoryActionBase):
    value: Optional[type_str] = Field(description="The value of the node history action")

    _prevent_none: classmethod = validators.prevent_none("value")
