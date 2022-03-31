from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class QueueBase(BaseModel):
    """Represents a queue used to separate various things (alerts, events, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the queue")

    value: type_str = Field(description="The value of the queue")


class QueueCreate(QueueBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the queue")


class QueueRead(QueueBase):
    uuid: UUID4 = Field(description="The UUID of the queue")

    class Config:
        orm_mode = True


class QueueUpdate(QueueBase):
    value: Optional[type_str] = Field(description="The value of the queue")

    _prevent_none: classmethod = validators.prevent_none("value")
