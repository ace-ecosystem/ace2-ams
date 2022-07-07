from datetime import datetime
from pydantic import BaseModel, Field, Json, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.alert_disposition import AlertDispositionRead
from api_models.analysis import RootAnalysisSubmissionTreeRead
from api_models.event import EventRead
from api_models.metadata_detection_point import MetadataDetectionPointRead
from api_models.observable import ObservableCreateInSubmission
from api_models.queue import QueueRead
from api_models.submission_comment import SubmissionCommentRead
from api_models.submission_tool import SubmissionToolRead
from api_models.submission_tool_instance import SubmissionToolInstanceRead
from api_models.submission_type import SubmissionTypeRead
from api_models.metadata_tag import MetadataTagRead
from api_models.user import UserRead


class SubmissionMatchingEventIndividual(BaseModel):
    """Represents an individual matched event that contains observables found in this submission."""

    event: EventRead = Field(description="The matched event")

    count: int = Field(description="The number of observables from this submission that are in the event")

    percent: int = Field(description="The percent of observables from this submission that are in the event")


class SubmissionMatchingEventByStatus(BaseModel):
    """Groups matching events by their status."""

    status: type_str = Field(description="The status of the matching events")

    events: list[SubmissionMatchingEventIndividual] = Field(
        default_factory=list, description="A list of matching events that have the same status"
    )


class SubmissionBase(BaseModel):
    """Represents a submission, which is an analysis request from the ACE Core or one manually created by an analyst."""

    alert: bool = Field(description="Whether or not this submission is an alert", default=False)

    description: Optional[type_str] = Field(description="A short description of the submission")

    event_time: datetime = Field(
        default_factory=datetime.utcnow, description="The time the activity in the submission occurred"
    )

    insert_time: datetime = Field(default_factory=datetime.utcnow, description="The time the submission was created")

    instructions: Optional[type_str] = Field(
        description="""An optional human readable list of instructions that an analyst should perform when manually
            reviewing this submission."""
    )

    queue: type_str = Field(description="The queue containing this submission")

    owner: Optional[type_str] = Field(description="The username of the user who has taken ownership of this submission")

    version: UUID4 = Field(
        default_factory=uuid4,
        description="""A version string that automatically changes every time the submission is modified.""",
    )


class SubmissionCreate(SubmissionBase):
    details: Optional[Json] = Field(description="A JSON representation of the root analysis details")

    history_username: Optional[type_str] = Field(
        description="If given, a submission history record will be created and associated with the user"
    )

    name: type_str = Field(description="The name of the submission")

    observables: list[ObservableCreateInSubmission] = Field(
        default_factory=list, description="A list of observables that should be added to the submission"
    )

    tags: list[type_str] = Field(default_factory=list, description="A list of tags to add to the submission")

    tool: Optional[type_str] = Field(description="The tool that created this submission")

    tool_instance: Optional[type_str] = Field(description="The instance of the tool that created this submission")

    type: type_str = Field(description="The type of this submission")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the submission")


class SubmissionRead(SubmissionBase):
    child_analysis_tags: list[MetadataTagRead] = Field(
        description="A list of tags added to observables by analysis modules", default_factory=list
    )

    child_detection_points: list[MetadataDetectionPointRead] = Field(
        description="A list of detection points added to child observables in the submission's tree",
        default_factory=list,
    )

    child_tags: list[MetadataTagRead] = Field(description="A list of tags added to observables", default_factory=list)

    comments: list[SubmissionCommentRead] = Field(
        description="A list of comments added to the submission", default_factory=list
    )

    disposition: Optional[AlertDispositionRead] = Field(description="The disposition assigned to this submission")

    disposition_time: Optional[datetime] = Field(description="The time this submission was most recently dispositioned")

    disposition_user: Optional[UserRead] = Field(description="The user who most recently dispositioned this submission")

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this submission")

    name: type_str = Field(description="""The name of the submission""")

    # Set a static string value so code displaying the tree structure knows which type of object this is.
    object_type: str = "submission"

    owner: Optional[UserRead] = Field(description="The user who has taken ownership of this submission")

    ownership_time: Optional[datetime] = Field(
        description="The time an analyst most recently took ownership of this submission"
    )

    queue: QueueRead = Field(description="The queue containing this submission")

    tags: list[MetadataTagRead] = Field(description="A list of tags added to the submission", default_factory=list)

    tool: Optional[SubmissionToolRead] = Field(description="The tool that created this submission")

    tool_instance: Optional[SubmissionToolInstanceRead] = Field(
        description="The instance of the tool that created this submission"
    )

    type: SubmissionTypeRead = Field(description="The type of this submission")

    uuid: UUID4 = Field(description="The UUID of the submission")

    class Config:
        orm_mode = True


class SubmissionUpdate(SubmissionBase):
    disposition: Optional[type_str] = Field(description="The disposition assigned to this submission")

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this submission")

    history_username: Optional[type_str] = Field(
        description="If given, a submission history record will be created and associated with the user"
    )

    queue: Optional[type_str] = Field(description="The submission queue containing this submission")

    tags: Optional[list[type_str]] = Field(description="A list of tags to add to the submission")

    uuid: UUID4 = Field(description="The UUID of the submission to update")

    # The version is optional when updating a submission since certain actions in the GUI do not need to care
    # about the version. However, if the version is given, the update will be rejected if it does not match.
    version: Optional[UUID4] = Field(
        description="""A version string that automatically changes every time the submission is modified. If supplied,
        the version must match when updating.""",
    )

    _prevent_none: classmethod = validators.prevent_none("queue", "tags")


class SubmissionTreeRead(SubmissionRead):
    matching_events: list[SubmissionMatchingEventByStatus] = Field(
        default_factory=list,
        description="A list of the events grouped by their status that contain observables found in this submission",
    )

    number_of_observables: int = Field(description="The total number of unique observables in the submission")

    root_analysis: RootAnalysisSubmissionTreeRead = Field(description="The submission's root analysis")

    class Config:
        orm_mode = True


class SubmissionVersion(BaseModel):
    version: UUID4 = Field(description="The current version of the submission")

    class Config:
        orm_mode = True
