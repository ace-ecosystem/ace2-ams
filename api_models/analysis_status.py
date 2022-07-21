from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class AnalysisStatusBase(BaseModel):
    """Represents a status that is applied to an analysis."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the analysis status")

    value: type_str = Field(description="The value of the analysis status")


class AnalysisStatusCreate(AnalysisStatusBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the analysis status")


class AnalysisStatusRead(AnalysisStatusBase):
    uuid: UUID4 = Field(description="The UUID of the analysis status")

    class Config:
        orm_mode = True


class AnalysisStatusUpdate(AnalysisStatusBase):
    value: Optional[type_str] = Field(description="The value of the analysis status")

    _prevent_none: classmethod = validators.prevent_none("value")
