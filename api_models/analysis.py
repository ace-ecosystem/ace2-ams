from datetime import datetime
from pydantic import Field, Json, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str
from api_models.analysis_module_type import AnalysisModuleTypeNodeTreeRead, AnalysisModuleTypeRead
from api_models.node import NodeBase, NodeCreate, NodeRead, NodeTreeItemRead, NodeUpdate
from api_models.node_detection_point import NodeDetectionPointRead


class AnalysisBase(NodeBase):
    """Represents an individual analysis that was performed."""

    details: Optional[Json] = Field(description="A JSON representation of the details produced by the analysis")

    error_message: Optional[type_str] = Field(description="An optional error message that occurred during analysis")

    stack_trace: Optional[type_str] = Field(description="An optional stack trace that occurred during analysis")

    summary: Optional[type_str] = Field(description="A short summary/description of what this analysis did or found")


class AnalysisCreate(NodeCreate, AnalysisBase):
    analysis_module_type_uuid: UUID4 = Field(
        description="""The UUID of the analysis module type that was used to perform this analysis."""
    )

    child_observables: "list[ObservableCreate]" = Field(
        default_factory=list, description="A list of child observables discovered during the analysis"
    )

    parent_observable_uuid: UUID4 = Field(description="The UUID of the target observable for this analysis")

    root_analysis_uuid: UUID4 = Field(description="The UUID of the Root Analysis that will contain this analysis")

    run_time: datetime = Field(description="The time at which the analysis was performed")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the analysis")


class AnalysisNodeTreeRead(NodeTreeItemRead):
    """Model used to control which information for an Analysis is displayed when getting an alert tree"""

    analysis_module_type: Optional[AnalysisModuleTypeNodeTreeRead] = Field(
        description="The analysis module type that was used to perform this analysis"
    )

    uuid: UUID4 = Field(description="The UUID of the analysis")

    class Config:
        orm_mode = True


class AnalysisRead(NodeRead, AnalysisBase):
    analysis_module_type: Optional[AnalysisModuleTypeRead] = Field(
        description="The analysis module type that was used to perform this analysis"
    )

    cached_until: datetime = Field(description="The time at which the analysis expires from the cache")

    child_observables: "list[ObservableRead]" = Field(
        description="The list of child observables produced by this analysis"
    )

    details: Optional[dict] = Field(description="A JSON representation of the details produced by the analysis")

    detection_points: list[NodeDetectionPointRead] = Field(
        description="A list of detection points added to the analysis"
    )

    run_time: datetime = Field(description="The time at which the analysis was performed")

    uuid: UUID4 = Field(description="The UUID of the analysis")

    class Config:
        orm_mode = True


class AnalysisUpdate(NodeUpdate, AnalysisBase):
    details: Optional[Json] = Field(description="A JSON representation of the details produced by the analysis")

    error_message: Optional[type_str] = Field(description="An optional error message that occurred during analysis")

    stack_trace: Optional[type_str] = Field(description="An optional stack trace that occurred during analysis")


# Needed for the circular relationship between analysis <-> observable
from api_models.observable import ObservableCreate, ObservableRead

AnalysisCreate.update_forward_refs()
AnalysisRead.update_forward_refs()
