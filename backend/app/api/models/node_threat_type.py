from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class NodeThreatTypeBase(BaseModel):
    """Represents a type that can be applied to a threat (fraud, keylogger, ransomware, etc)."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node threat type"
    )

    value: type_str = Field(description="The value of the node threat type")


class NodeThreatTypeCreate(NodeThreatTypeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node threat type")


class NodeThreatTypeRead(NodeThreatTypeBase):
    uuid: UUID4 = Field(description="The UUID of the node threat type")

    class Config:
        orm_mode = True


class NodeThreatTypeUpdate(NodeThreatTypeBase):
    value: Optional[type_str] = Field(description="The value of the node threat type")

    _prevent_none: classmethod = validators.prevent_none("value")
