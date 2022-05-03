from datetime import datetime
from pydantic import Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.alert_disposition import AlertDispositionRead
from api_models.alert_tool import AlertToolRead
from api_models.alert_tool_instance import AlertToolInstanceRead
from api_models.alert_type import AlertTypeRead
from api_models.node import NodeBase, NodeCreate, NodeRead, NodeTreeItemRead, NodeUpdate
from api_models.node_comment import NodeCommentRead
from api_models.node_tag import NodeTagRead
from api_models.node_threat import NodeThreatRead
from api_models.node_threat_actor import NodeThreatActorRead
from api_models.observable import ObservableCreate
from api_models.queue import QueueRead
from api_models.user import UserRead


class AlertBase(NodeBase):
    """Represents an alert, which is a RootAnalysis from the ACE Core or one manually created by an analyst."""

    description: Optional[type_str] = Field(description="A short description of the alert")

    event_time: datetime = Field(
        default_factory=datetime.utcnow, description="The time the activity alerted on occurred"
    )

    insert_time: datetime = Field(default_factory=datetime.utcnow, description="The time the alert was created")

    instructions: Optional[type_str] = Field(
        description="""An optional human readable list of instructions that an analyst should perform when manually
            reviewing this alert."""
    )

    queue: type_str = Field(description="The alert queue containing this alert")

    owner: Optional[type_str] = Field(description="The username of the user who has taken ownership of this alert")


class AlertCreate(NodeCreate, AlertBase):
    history_username: Optional[type_str] = Field(
        description="If given, an alert history record will be created and associated with the user"
    )

    name: type_str = Field(description="""The name of the alert""")

    root_observables: List[ObservableCreate] = Field(
        description="A list of observables that should be added to the alert"
    )

    tags: List[type_str] = Field(default_factory=list, description="A list of tags to add to the alert")

    threat_actors: List[type_str] = Field(
        default_factory=list, description="A list of threat actors to add to the alert"
    )

    threats: List[type_str] = Field(default_factory=list, description="A list of threats to add to the alert")

    tool: Optional[type_str] = Field(description="The tool that created this alert")

    tool_instance: Optional[type_str] = Field(description="The instance of the tool that created this alert")

    type: type_str = Field(description="The type of this alert")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the alert")


class AlertRead(NodeRead, AlertBase):
    child_tags: List[NodeTagRead] = Field(description="A list of tags added to child Nodes in the alert's tree")

    child_threat_actors: List[NodeThreatActorRead] = Field(
        description="A list of threat actors added to child Nodes in the alert's tree"
    )

    child_threats: List[NodeThreatRead] = Field(
        description="A list of threats added to child Nodes in the alert's tree"
    )

    comments: List[NodeCommentRead] = Field(description="A list of comments added to the alert", default_factory=list)

    disposition: Optional[AlertDispositionRead] = Field(description="The disposition assigned to this alert")

    disposition_time: Optional[datetime] = Field(description="The time this alert was most recently dispositioned")

    disposition_user: Optional[UserRead] = Field(description="The user who most recently dispositioned this alert")

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this alert")

    name: type_str = Field(description="""The name of the alert""")

    owner: Optional[UserRead] = Field(description="The user who has taken ownership of this alert")

    queue: QueueRead = Field(description="The queue containing this alert")

    tags: List[NodeTagRead] = Field(description="A list of tags added to the alert")

    threat_actors: List[NodeThreatActorRead] = Field(description="A list of threat actors added to the alert")

    threats: List[NodeThreatRead] = Field(description="A list of threats added to the alert")

    tool: Optional[AlertToolRead] = Field(description="The tool that created this alert")

    tool_instance: Optional[AlertToolInstanceRead] = Field(
        description="The instance of the tool that created this alert"
    )

    type: AlertTypeRead = Field(description="The type of this alert")

    uuid: UUID4 = Field(description="The UUID of the alert")

    class Config:
        orm_mode = True


class AlertUpdate(NodeUpdate, AlertBase):
    disposition: Optional[type_str] = Field(description="The disposition assigned to this alert")

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this alert")

    queue: Optional[type_str] = Field(description="The alert queue containing this alert")

    tags: Optional[List[type_str]] = Field(description="A list of tags to add to the alert")

    threat_actors: Optional[List[type_str]] = Field(description="A list of threat actors to add to the alert")

    threats: Optional[List[type_str]] = Field(description="A list of threats to add to the alert")

    _prevent_none: classmethod = validators.prevent_none("queue", "tags", "threat_actors", "threats")


class AlertUpdateMultiple(AlertUpdate):
    uuid: UUID4 = Field(description="The UUID of the alert")


class AlertTreeRead(AlertRead, NodeTreeItemRead):
    class Config:
        orm_mode = True
