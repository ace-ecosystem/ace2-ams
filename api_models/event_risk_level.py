from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class EventRiskLevelBase(BaseModel):
    """Represents a risk level that can be applied to an event to denote its severity."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event risk level"
    )

    value: type_str = Field(description="The value of the event risk level")


class EventRiskLevelCreate(EventRiskLevelBase):
    queues: type_list_str = Field(description="The event queues where this risk level is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event risk level")


class EventRiskLevelRead(EventRiskLevelBase):
    uuid: UUID4 = Field(description="The UUID of the event risk level")

    queues: List[QueueRead] = Field(description="The event queues where this risk level is valid")

    class Config:
        orm_mode = True


class EventRiskLevelUpdate(EventRiskLevelBase):
    queues: Optional[type_list_str] = Field(description="The event queues where this risk level is valid")

    value: Optional[type_str] = Field(description="The value of the event risk level")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
