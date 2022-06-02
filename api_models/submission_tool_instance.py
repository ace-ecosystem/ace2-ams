from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class SubmissionToolInstanceBase(BaseModel):
    """Represents a type of submission."""

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the submission tool instance"
    )

    value: type_str = Field(description="The value of the submission tool instance")


class SubmissionToolInstanceCreate(SubmissionToolInstanceBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the submission tool instance")


class SubmissionToolInstanceRead(SubmissionToolInstanceBase):
    uuid: UUID4 = Field(description="The UUID of the submission tool instance")

    class Config:
        orm_mode = True


class SubmissionToolInstanceUpdate(SubmissionToolInstanceBase):
    value: Optional[type_str] = Field(description="The value of the submission tool instance")

    _prevent_none: classmethod = validators.prevent_none("value")
