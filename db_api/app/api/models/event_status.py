from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api.models import type_str, type_list_str, validators
from api.models.queue import QueueRead


class EventStatusBase(BaseModel):
    """Represents a status that can be applied to an event (open, closed, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event status")

    value: type_str = Field(description="The value of the event status")


class EventStatusCreate(EventStatusBase):
    queues: type_list_str = Field(description="The event queues where this status is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event status")


class EventStatusRead(EventStatusBase):
    uuid: UUID4 = Field(description="The UUID of the event status")

    queues: List[QueueRead] = Field(description="The event queues where this status is valid")

    class Config:
        orm_mode = True


class EventStatusUpdate(EventStatusBase):
    queues: Optional[type_list_str] = Field(description="The event queues where this status is valid")

    value: Optional[type_str] = Field(description="The value of the event status")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
