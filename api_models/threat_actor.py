from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class ThreatActorBase(BaseModel):
    """Represents a threat actor that can be applied to a an object."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the threat actor")

    value: type_str = Field(description="The value of the threat actor")


class ThreatActorCreate(ThreatActorBase):
    queues: type_list_str = Field(description="The queues where this threat actor is valid")

    uuid: UUID4 = Field(default_factory=uuid4, escription="The UUID of the threat actor")


class ThreatActorRead(ThreatActorBase):
    uuid: UUID4 = Field(description="The UUID of the threat actor")

    queues: list[QueueRead] = Field(description="The queues where this threat actor is valid")

    class Config:
        orm_mode = True


class ThreatActorUpdate(ThreatActorBase):
    queues: Optional[type_list_str] = Field(description="The queues where this threat actor is valid")

    value: Optional[type_str] = Field(description="The value of the threat actor")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
