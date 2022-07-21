from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class EventSourceBase(BaseModel):
    """Represents a source that can be applied to an event (phishing, host compromise, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event source")

    value: type_str = Field(description="The value of the event source")


class EventSourceCreate(EventSourceBase):
    queues: type_list_str = Field(description="The event queues where this source is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event source")


class EventSourceRead(EventSourceBase):
    uuid: UUID4 = Field(description="The UUID of the event source")

    queues: list[QueueRead] = Field(description="The event queues where this source is valid")

    class Config:
        orm_mode = True


class EventSourceUpdate(EventSourceBase):
    queues: Optional[type_list_str] = Field(description="The event queues where this source is valid")

    value: Optional[type_str] = Field(description="The value of the event source")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
