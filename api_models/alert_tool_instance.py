from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class AlertToolInstanceBase(BaseModel):
    """Represents a type of alert."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the alert tool instance"
    )

    value: type_str = Field(description="The value of the alert tool instance")


class AlertToolInstanceCreate(AlertToolInstanceBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the alert tool instance")


class AlertToolInstanceRead(AlertToolInstanceBase):
    uuid: UUID4 = Field(description="The UUID of the alert tool instance")

    class Config:
        orm_mode = True


class AlertToolInstanceUpdate(AlertToolInstanceBase):
    value: Optional[type_str] = Field(description="The value of the alert tool instance")

    _prevent_none: classmethod = validators.prevent_none("value")
