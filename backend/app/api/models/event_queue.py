from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class EventQueueBase(BaseModel):
    """Represents an event queue used to filter events."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event queue")

    value: type_str = Field(description="The value of the event queue")


class EventQueueCreate(EventQueueBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event queue")


class EventQueueRead(EventQueueBase):
    uuid: UUID4 = Field(description="The UUID of the event queue")

    class Config:
        orm_mode = True


class EventQueueUpdate(EventQueueBase):
    value: Optional[type_str] = Field(description="The value of the event queue")

    _prevent_none: classmethod = validators.prevent_none("value")
