from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class ThreatTypeBase(BaseModel):
    """Represents a type that can be applied to a threat (fraud, keylogger, ransomware, etc)."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node threat type"
    )

    value: type_str = Field(description="The value of the node threat type")


class ThreatTypeCreate(ThreatTypeBase):
    queues: type_list_str = Field(description="The queues where this node threat type is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node threat type")


class ThreatTypeRead(ThreatTypeBase):
    uuid: UUID4 = Field(description="The UUID of the node threat type")

    queues: list[QueueRead] = Field(description="The queues where this node threat type is valid")

    class Config:
        orm_mode = True


class ThreatTypeUpdate(ThreatTypeBase):
    queues: Optional[type_list_str] = Field(description="The queues where this node threat type is valid")

    value: Optional[type_str] = Field(description="The value of the node threat type")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
