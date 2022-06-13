from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class EventSeverityBase(BaseModel):
    """Represents a severity that can be applied to an event to denote its severity."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event severity"
    )

    value: type_str = Field(description="The value of the event severity")


class EventSeverityCreate(EventSeverityBase):
    queues: type_list_str = Field(description="The event queues where this severity is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event severity")


class EventSeverityRead(EventSeverityBase):
    uuid: UUID4 = Field(description="The UUID of the event severity")

    queues: list[QueueRead] = Field(description="The event queues where this severity is valid")

    class Config:
        orm_mode = True


class EventSeverityUpdate(EventSeverityBase):
    queues: Optional[type_list_str] = Field(description="The event queues where this severity is valid")

    value: Optional[type_str] = Field(description="The value of the event severity")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
