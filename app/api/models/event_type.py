from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class EventTypeBase(BaseModel):
    """Represents a type that can be applied to an event (phishing, host compromise, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event type")

    value: type_str = Field(description="The value of the event type")


class EventTypeCreate(EventTypeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event type")


class EventTypeRead(EventTypeBase):
    uuid: UUID4 = Field(description="The UUID of the event type")

    class Config:
        orm_mode = True


class EventTypeUpdate(EventTypeBase):
    value: Optional[type_str] = Field(description="The value of the event type")

    _prevent_none: classmethod = validators.prevent_none("value")
