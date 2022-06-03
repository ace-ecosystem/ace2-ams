from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class SubmissionTypeBase(BaseModel):
    """Represents a type of submission."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the submission type")

    value: type_str = Field(description="The value of the submission type")


class SubmissionTypeCreate(SubmissionTypeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the submission type")


class SubmissionTypeRead(SubmissionTypeBase):
    uuid: UUID4 = Field(description="The UUID of the submission type")

    class Config:
        orm_mode = True


class SubmissionTypeUpdate(SubmissionTypeBase):
    value: Optional[type_str] = Field(description="The value of the submission type")

    _prevent_none: classmethod = validators.prevent_none("value")
