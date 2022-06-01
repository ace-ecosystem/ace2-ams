from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class EventVectorBase(BaseModel):
    """Represents a vector that can be applied to an event to denote how the attack was initiated (email, usb, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event vector")

    value: type_str = Field(description="The value of the event vector")


class EventVectorCreate(EventVectorBase):
    queues: type_list_str = Field(description="The event queues where this vector is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event vector")


class EventVectorRead(EventVectorBase):
    uuid: UUID4 = Field(description="The UUID of the event vector")

    queues: list[QueueRead] = Field(description="The event queues where this vector is valid")

    class Config:
        orm_mode = True


class EventVectorUpdate(EventVectorBase):
    queues: Optional[type_list_str] = Field(description="The event queues where this vector is valid")

    value: Optional[type_str] = Field(description="The value of the event vector")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
