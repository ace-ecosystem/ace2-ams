from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class EventTypeBase(BaseModel):
    """Represents a type that can be applied to an event (phishing, host compromise, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event type")

    value: type_str = Field(description="The value of the event type")


class EventTypeCreate(EventTypeBase):
    queues: type_list_str = Field(description="The event queues where this type is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event type")


class EventTypeRead(EventTypeBase):
    uuid: UUID4 = Field(description="The UUID of the event type")

    queues: list[QueueRead] = Field(description="The event queues where this type is valid")

    class Config:
        orm_mode = True


class EventTypeUpdate(EventTypeBase):
    queues: Optional[type_list_str] = Field(description="The event queues where this type is valid")

    value: Optional[type_str] = Field(description="The value of the event type")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
