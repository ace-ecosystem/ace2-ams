from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api.models import type_str, type_list_str, validators
from api.models.queue import QueueRead


class NodeThreatActorBase(BaseModel):
    """Represents a threat actor that can be applied to a node."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the node threat actor"
    )

    value: type_str = Field(description="The value of the node threat actor")


class NodeThreatActorCreate(NodeThreatActorBase):
    queues: type_list_str = Field(description="The queues where this node threat actor is valid")

    uuid: UUID4 = Field(default_factory=uuid4, escription="The UUID of the node threat actor")


class NodeThreatActorRead(NodeThreatActorBase):
    uuid: UUID4 = Field(description="The UUID of the node threat actor")

    queues: List[QueueRead] = Field(description="The queues where this node threat actor is valid")

    class Config:
        orm_mode = True


class NodeThreatActorUpdate(NodeThreatActorBase):
    queues: Optional[type_list_str] = Field(description="The queues where this node threat actor is valid")

    value: Optional[type_str] = Field(description="The value of the node threat actor")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
