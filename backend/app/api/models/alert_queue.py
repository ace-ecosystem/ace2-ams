from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators


class AlertQueueBase(BaseModel):
    """Represents an alert queue used to filter alerts (typically by an analyst's job function)."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the alert queue")

    value: type_str = Field(description="The value of the alert queue")


class AlertQueueCreate(AlertQueueBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the alert queue")


class AlertQueueRead(AlertQueueBase):
    uuid: UUID4 = Field(description="The UUID of the alert queue")

    class Config:
        orm_mode = True


class AlertQueueUpdate(AlertQueueBase):
    value: Optional[type_str] = Field(description="The value of the alert queue")

    _prevent_none: classmethod = validators.prevent_none("value")
