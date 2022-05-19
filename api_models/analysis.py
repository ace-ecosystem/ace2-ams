from datetime import datetime
from pydantic import BaseModel, Field, Json, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str
from api_models.analysis_module_type import AnalysisModuleTypeRead


class AnalysisBase(BaseModel):
    """Represents an individual analysis that was performed."""

    details: Optional[Json] = Field(description="A JSON representation of the details produced by the analysis")

    error_message: Optional[type_str] = Field(description="An optional error message that occurred during analysis")

    stack_trace: Optional[type_str] = Field(description="An optional stack trace that occurred during analysis")

    summary: Optional[type_str] = Field(description="A short summary/description of what this analysis did or found")


class AnalysisCreate(AnalysisBase):
    analysis_module_type_uuid: UUID4 = Field(
        description="""The UUID of the analysis module type that was used to perform this analysis"""
    )

    child_observables: "list[ObservableCreate]" = Field(
        default_factory=list, description="A list of child observables discovered during the analysis"
    )

    run_time: datetime = Field(description="The time at which the analysis was performed")

    submission_uuid: UUID4 = Field(description="The UUID of the submission that will contain this analysis")

    target_uuid: UUID4 = Field(description="The UUID of the target observable for this analysis")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the analysis")


class AnalysisRead(AnalysisBase):
    analysis_module_type: Optional[AnalysisModuleTypeRead] = Field(
        description="The analysis module type that was used to perform this analysis"
    )

    cached_until: datetime = Field(description="The time at which the analysis expires from the cache")

    child_observables: "list[ObservableRead]" = Field(
        description="The list of child observables produced by this analysis"
    )

    details: Optional[dict] = Field(description="A JSON representation of the details produced by the analysis")

    # Set a static string value so code displaying the tree structure knows which type of object this is.
    # This is needed (for now) because the Analysis table no longer inherits from the Node table.
    node_type: str = "analysis"

    run_time: datetime = Field(description="The time at which the analysis was performed")

    uuid: UUID4 = Field(description="The UUID of the analysis")

    class Config:
        orm_mode = True


class AnalysisUpdate(AnalysisBase):
    details: Optional[Json] = Field(description="A JSON representation of the details produced by the analysis")

    error_message: Optional[type_str] = Field(description="An optional error message that occurred during analysis")

    stack_trace: Optional[type_str] = Field(description="An optional stack trace that occurred during analysis")


# Needed for the circular relationship between analysis <-> observable
from api_models.observable import ObservableCreate, ObservableRead

AnalysisCreate.update_forward_refs()
AnalysisRead.update_forward_refs()
