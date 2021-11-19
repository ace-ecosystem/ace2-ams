from pydantic import Field, Json, UUID4
from typing import Optional
from uuid import uuid4

from pydantic.main import BaseModel

from api.models import type_str
from api.models.analysis_module_type import AnalysisModuleTypeAlertTreeRead, AnalysisModuleTypeRead
from api.models.node import NodeBase, NodeCreate, NodeRead, NodeUpdate


class AnalysisBase(NodeBase):
    """Represents an individual analysis that was performed."""

    analysis_module_type: Optional[UUID4] = Field(
        description="""The UUID of the analysis module type that was used to perform this analysis. This can be NULL in
            the case of manually created alerts."""
    )

    summary: Optional[type_str] = Field(description="A short summary/description of what this analysis did or found")


class AnalysisCreate(NodeCreate, AnalysisBase):
    alert_uuid: UUID4 = Field(description="The UUID of the alert containing this analysis")

    details: Optional[Json] = Field(description="A JSON representation of the details produced by the analysis")

    error_message: Optional[type_str] = Field(description="An optional error message that occurred during analysis")

    # TODO - save for the end, still need to flesh out this functionality
    # event_summary: Optional[AnalysisEventSummary] = Field(
    #     description="""Optional summary information to display on an event page if this analysis is ever added to an
    #     event"""
    # )

    parent_uuid: Optional[UUID4] = Field(description="The UUID of the observable containing this analysis")

    stack_trace: Optional[type_str] = Field(description="An optional stack trace that occurred during analysis")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the analysis")


class AnalysisAlertTreeRead(BaseModel):
    """Model used to control which information for an Analysis is displayed when getting an alert tree"""

    analysis_module_type: Optional[AnalysisModuleTypeAlertTreeRead] = Field(
        description="The analysis module type that was used to perform this analysis"
    )

    parent_uuid: Optional[UUID4] = Field(description="The UUID of the observable containing this analysis")

    uuid: UUID4 = Field(description="The UUID of the analysis")

    class Config:
        orm_mode = True


class AnalysisRead(NodeRead, AnalysisBase):
    alert_uuid: UUID4 = Field(description="The UUID of the alert containing this analysis")

    analysis_module_type: Optional[AnalysisModuleTypeRead] = Field(
        description="The analysis module type that was used to perform this analysis"
    )

    parent_uuid: Optional[UUID4] = Field(description="The UUID of the observable containing this analysis")

    uuid: UUID4 = Field(description="The UUID of the analysis")

    class Config:
        orm_mode = True


class AnalysisUpdate(NodeUpdate, AnalysisBase):
    details: Optional[Json] = Field(description="A JSON representation of the details produced by the analysis")

    error_message: Optional[type_str] = Field(description="An optional error message that occurred during analysis")

    # TODO - save for the end, still need to flesh out this functionality
    # event_summary: Optional[AnalysisEventSummary] = Field(
    #     description="""Optional summary information to display on an event page if this analysis is ever added to an
    #     event"""
    # )

    stack_trace: Optional[type_str] = Field(description="An optional stack trace that occurred during analysis")
