from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class SubmissionToolBase(BaseModel):
    """Represents a type of submission."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the submission tool")

    value: type_str = Field(description="The value of the submission tool")


class SubmissionToolCreate(SubmissionToolBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the submission tool")


class SubmissionToolRead(SubmissionToolBase):
    uuid: UUID4 = Field(description="The UUID of the submission tool")

    class Config:
        orm_mode = True


class SubmissionToolUpdate(SubmissionToolBase):
    value: Optional[type_str] = Field(description="The value of the submission tool")

    _prevent_none: classmethod = validators.prevent_none("value")
