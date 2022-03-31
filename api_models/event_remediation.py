from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api_models import type_str, type_list_str, validators
from api_models.queue import QueueRead


class EventRemediationBase(BaseModel):
    """Represents a remediation that can be applied to an event to denote which tasks were taken to clean up after
    the attack."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the event remediation"
    )

    value: type_str = Field(description="The value of the event remediation")


class EventRemediationCreate(EventRemediationBase):
    queues: type_list_str = Field(description="The event queues where this remediation is valid")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event remediation")


class EventRemediationRead(EventRemediationBase):
    uuid: UUID4 = Field(description="The UUID of the event remediation")

    queues: List[QueueRead] = Field(description="The event queues where this remediation is valid")

    class Config:
        orm_mode = True


class EventRemediationUpdate(EventRemediationBase):
    queues: Optional[type_list_str] = Field(description="The event queues where this remediation is valid")

    value: Optional[type_str] = Field(description="The value of the event remediation")

    _prevent_none: classmethod = validators.prevent_none("queues", "value")
