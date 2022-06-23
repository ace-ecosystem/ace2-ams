from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_list_str, type_str, validators
from api_models.threat_type import ThreatTypeRead
from api_models.queue import QueueRead


class ThreatBase(BaseModel):
    """Represents a threat that can be applied to an object to denote things like a family of malware or specific type
    of attack."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the threat")

    types: type_list_str = Field(description="A list of types the threat represents")

    value: type_str = Field(description="The value of the threat")


class ThreatCreate(ThreatBase):
    queues: type_list_str = Field(description="The queues where this threat is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the threat")


class ThreatRead(ThreatBase):
    queues: list[QueueRead] = Field(description="The queues where this threat is valid")

    types: list[ThreatTypeRead] = Field(description="A list of types the threat represents")

    uuid: UUID4 = Field(description="The UUID of the threat")

    class Config:
        orm_mode = True


class ThreatUpdate(ThreatBase):
    queues: Optional[type_list_str] = Field(description="The queues where this threat is valid")

    types: Optional[type_list_str] = Field(description="A list of types the threat represents")

    value: Optional[type_str] = Field(description="The value of the threat")

    _prevent_none: classmethod = validators.prevent_none("queues", "types", "value")
