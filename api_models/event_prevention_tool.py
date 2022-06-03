from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class EventPreventionToolBase(BaseModel):
    """Represents a prevention tool that can be applied to an event to denote which tool or process stopped the
    attack."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event prevention tool"
    )

    value: type_str = Field(description="The value of the event prevention tool")


class EventPreventionToolCreate(EventPreventionToolBase):
    queues: type_list_str = Field(description="The queues where this prevention tool is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event prevention tool")


class EventPreventionToolRead(EventPreventionToolBase):
    uuid: UUID4 = Field(description="The UUID of the event prevention tool")

    queues: list[QueueRead] = Field(description="The queues where this prevention tool is valid")

    class Config:
        orm_mode = True


class EventPreventionToolUpdate(EventPreventionToolBase):
    queues: Optional[type_list_str] = Field(description="The queues where this prevention tool is valid")

    value: Optional[type_str] = Field(description="The value of the event prevention tool")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
