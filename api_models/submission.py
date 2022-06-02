from datetime import datetime
from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.alert_disposition import AlertDispositionRead
from api_models.node import NodeBase, NodeCreate, NodeRead, NodeUpdate
from api_models.node_comment import NodeCommentRead
from api_models.node_tag import NodeTagRead
from api_models.node_threat import NodeThreatRead
from api_models.node_threat_actor import NodeThreatActorRead
from api_models.observable import ObservableCreate
from api_models.queue import QueueRead
from api_models.submission_tool import SubmissionToolRead
from api_models.submission_tool_instance import SubmissionToolInstanceRead
from api_models.submission_type import SubmissionTypeRead
from api_models.user import UserRead


class SubmissionBase(NodeBase):
    """Represents a submission, which is an analysis request from the ACE Core or one manually created by an analyst."""

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


class SubmissionCreate(NodeCreate, SubmissionBase):
    history_username: Optional[type_str] = Field(
        description="If given, a submission history record will be created and associated with the user"
    )

    name: type_str = Field(description="The name of the submission")

    observables: list[ObservableCreate] = Field(
        default_factory=list, description="A list of observables that should be added to the submission"
    )

    tags: list[type_str] = Field(default_factory=list, description="A list of tags to add to the submission")

    threat_actors: list[type_str] = Field(
        default_factory=list, description="A list of threat actors to add to the submission"
    )

    threats: list[type_str] = Field(default_factory=list, description="A list of threats to add to the submission")

    tool: Optional[type_str] = Field(description="The tool that created this submission")

    tool_instance: Optional[type_str] = Field(description="The instance of the tool that created this submission")

    type: type_str = Field(description="The type of this submission")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the submission")


class SubmissionRead(NodeRead, SubmissionBase):
    child_tags: list[NodeTagRead] = Field(
        description="A list of tags added to child Nodes in the submission's tree", default_factory=list
    )

    child_threat_actors: list[NodeThreatActorRead] = Field(
        description="A list of threat actors added to child Nodes in the submission's tree", default_factory=list
    )

    child_threats: list[NodeThreatRead] = Field(
        description="A list of threats added to child Nodes in the submission's tree", default_factory=list
    )

    comments: list[NodeCommentRead] = Field(
        description="A list of comments added to the submission", default_factory=list
    )

    disposition: Optional[AlertDispositionRead] = Field(description="The disposition assigned to this submission")

    disposition_time: Optional[datetime] = Field(description="The time this submission was most recently dispositioned")

    disposition_user: Optional[UserRead] = Field(description="The user who most recently dispositioned this submission")

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this submission")

    name: type_str = Field(description="""The name of the submission""")

    owner: Optional[UserRead] = Field(description="The user who has taken ownership of this submission")

    ownership_time: Optional[datetime] = Field(
        description="The time an analyst most recently took ownership of this submission"
    )

    queue: QueueRead = Field(description="The queue containing this submission")

    tags: list[NodeTagRead] = Field(description="A list of tags added to the submission", default_factory=list)

    threat_actors: list[NodeThreatActorRead] = Field(
        description="A list of threat actors added to the submission", default_factory=list
    )

    threats: list[NodeThreatRead] = Field(description="A list of threats added to the submission", default_factory=list)

    tool: Optional[SubmissionToolRead] = Field(description="The tool that created this submission")

    tool_instance: Optional[SubmissionToolInstanceRead] = Field(
        description="The instance of the tool that created this submission"
    )

    type: SubmissionTypeRead = Field(description="The type of this submission")

    uuid: UUID4 = Field(description="The UUID of the submission")

    class Config:
        orm_mode = True


class SubmissionUpdate(NodeUpdate, SubmissionBase):
    disposition: Optional[type_str] = Field(description="The disposition assigned to this submission")

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this submission")

    history_username: Optional[type_str] = Field(
        description="If given, a submission history record will be created and associated with the user"
    )

    queue: Optional[type_str] = Field(description="The submission queue containing this submission")

    tags: Optional[list[type_str]] = Field(description="A list of tags to add to the submission")

    threat_actors: Optional[list[type_str]] = Field(description="A list of threat actors to add to the submission")

    threats: Optional[list[type_str]] = Field(description="A list of threats to add to the submission")

    uuid: UUID4 = Field(description="The UUID of the submission to update")

    _prevent_none: classmethod = validators.prevent_none("queue", "tags", "threat_actors", "threats")


class SubmissionTreeRead(SubmissionRead):
    children: list[dict] = Field(default_factory=list, description="A list of this submission's child objects")

    class Config:
        orm_mode = True
