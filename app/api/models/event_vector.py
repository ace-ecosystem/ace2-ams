from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class EventVectorBase(BaseModel):
    """Represents a vector that can be applied to an event to denote how the attack was initiated (email, usb, etc)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the event vector")

    value: type_str = Field(description="The value of the event vector")


class EventVectorCreate(EventVectorBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event vector")


class EventVectorRead(EventVectorBase):
    uuid: UUID4 = Field(description="The UUID of the event vector")

    class Config:
        orm_mode = True


class EventVectorUpdate(EventVectorBase):
    value: Optional[type_str] = Field(description="The value of the event vector")

    _prevent_none: classmethod = validators.prevent_none("value")
