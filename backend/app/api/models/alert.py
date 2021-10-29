from datetime import datetime
from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators
from api.models.alert_disposition import AlertDispositionRead
from api.models.alert_queue import AlertQueueRead
from api.models.alert_tool import AlertToolRead
from api.models.alert_tool_instance import AlertToolInstanceRead
from api.models.alert_type import AlertTypeRead
from api.models.analysis import AnalysisRead
from api.models.node import NodeBase, NodeCreate, NodeRead, NodeUpdate
from api.models.user import UserRead


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

    name: Optional[type_str] = Field(
        description="""An optional property that defines a name for an alert. Used to track and document analyst
            response instructions."""
    )

    # TODO: When we have authentication, creating a manual alert will infer the owner from the token.
    owner: Optional[type_str] = Field(description="The username of the user who has taken ownership of this alert")

    queue: type_str = Field(description="The alert queue containing this alert")

    tool: Optional[type_str] = Field(description="The tool that created this alert")

    tool_instance: Optional[type_str] = Field(description="The instance of the tool that created this alert")

    type: type_str = Field(description="The type of this alert")


class AlertCreate(NodeCreate, AlertBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the alert")


class AlertRead(NodeRead, AlertBase):
    analysis: AnalysisRead = Field(description="The analysis representing this alert")

    disposition: Optional[AlertDispositionRead] = Field(description="The disposition assigned to this alert")

    disposition_time: Optional[datetime] = Field(description="The time this alert was most recently dispositioned")

    disposition_user: Optional[UserRead] = Field(description="The user who most recently dispositioned this alert")

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this alert")

    owner: Optional[UserRead] = Field(description="The user who has taken ownership of this alert")

    queue: AlertQueueRead = Field(description="The alert queue containing this alert")

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

    # TODO: This should not be editable. When we have authentication in place, the user will be inferred from the token.
    # disposition_user: Optional[type_str] = Field(
    #     description="The username of the user who most recently dispositioned this alert"
    # )

    event_uuid: Optional[UUID4] = Field(description="The UUID of the event containing this alert")

    queue: Optional[type_str] = Field(description="The alert queue containing this alert")

    type: Optional[type_str] = Field(description="The type of this alert")

    _prevent_none: classmethod = validators.prevent_none("queue", "type")
