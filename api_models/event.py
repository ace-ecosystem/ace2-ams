from datetime import datetime
from pydantic import Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.alert_disposition import AlertDispositionRead
from api_models.event_prevention_tool import EventPreventionToolRead
from api_models.event_remediation import EventRemediationRead
from api_models.event_risk_level import EventRiskLevelRead
from api_models.event_source import EventSourceRead
from api_models.event_status import EventStatusRead
from api_models.event_type import EventTypeRead
from api_models.event_vector import EventVectorRead
from api_models.node import NodeBase, NodeCreate, NodeRead, NodeUpdate
from api_models.node_comment import NodeCommentRead
from api_models.node_tag import NodeTagRead
from api_models.node_threat import NodeThreatRead
from api_models.node_threat_actor import NodeThreatActorRead
from api_models.queue import QueueRead
from api_models.user import UserRead


class EventBase(NodeBase):
    """Represents a collection of alerts that combine to form an attack."""

    alert_time: Optional[datetime] = Field(description="The time of the earliest alert in the event")

    contain_time: Optional[datetime] = Field(description="The time the attack represented by the event was contained")

    # TODO: Make this a calculated value based on the alerts as they get added to the event
    disposition_time: Optional[datetime] = Field(
        description="The earliest time one of the alerts in the event was dispositioned"
    )

    event_time: Optional[datetime] = Field(description="The time at which the attack represented by the event occurred")

    name: type_str = Field(description="The name of the event")

    owner: Optional[type_str] = Field(description="The username of the user who has taken ownership of this event")

    # TODO: Make this a calculated value based on the alerts as they are added to the event
    ownership_time: Optional[datetime] = Field(
        description="The earliest time an analyst took ownership over an alert in the event"
    )

    prevention_tools: List[type_str] = Field(
        default_factory=list, description="A list of prevention tools involved in the event"
    )

    queue: type_str = Field(description="The event queue containing this event")

    remediation_time: Optional[datetime] = Field(
        description="The earliest time that any remediation was performed on the attack represented by the event"
    )

    remediations: List[type_str] = Field(
        default_factory=list,
        description="A list of remediations performed to clean up the attack represented by the event",
    )

    risk_level: Optional[type_str] = Field(description="The risk level assigned to the event")

    source: Optional[type_str] = Field(description="The source of the event")

    status: type_str = Field(description="The status assigned to the event")

    type: Optional[type_str] = Field(description="The type assigned to the event")

    vectors: List[type_str] = Field(default_factory=list, description="A list of vectors assigned to the event")


class EventCreate(NodeCreate, EventBase):
    creation_time: datetime = Field(default_factory=datetime.utcnow, description="The time the event was created")

    history_username: Optional[type_str] = Field(
        description="If given, an event history record will be created and associated with the user"
    )

    tags: List[type_str] = Field(default_factory=list, description="A list of tags to add to the event")

    threat_actors: List[type_str] = Field(
        default_factory=list, description="A list of threat actors to add to the event"
    )

    threats: List[type_str] = Field(default_factory=list, description="A list of threats to add to the event")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the event")


class EventRead(NodeRead, EventBase):
    alert_uuids: List[UUID4] = Field(default_factory=list, description="A list of alert UUIDs contained in the event")

    analysis_types: List[str] = Field(
        description="A deduplicated list of analysis module types that exist within the event", default_factory=list
    )

    auto_alert_time: Optional[datetime] = Field(
        description="The automatically calculated time of the earliest insert time from the alerts in the event"
    )

    auto_disposition_time: Optional[datetime] = Field(
        description="The automatically calculated earliest time one of the alerts in the event was dispositioned"
    )

    auto_event_time: Optional[datetime] = Field(
        description="The automatically calculated time of the earliest event time from the alerts in the event"
    )

    auto_ownership_time: Optional[datetime] = Field(
        description="The automatically calculated earliest time an analyst took ownership of one of the alerts"
    )

    comments: List[NodeCommentRead] = Field(description="A list of comments added to the event", default_factory=list)

    creation_time: datetime = Field(description="The time the event was created")

    disposition: Optional[AlertDispositionRead] = Field(
        description="The highest disposition used on the alerts in the event"
    )

    owner: Optional[UserRead] = Field(description="The user who has taken ownership of this event")

    prevention_tools: List[EventPreventionToolRead] = Field(
        description="A list of prevention tools involved in the event"
    )

    queue: QueueRead = Field(description="The queue containing this event")

    remediations: List[EventRemediationRead] = Field(
        description="A list of remediations performed to clean up the attack represented by the event"
    )

    risk_level: Optional[EventRiskLevelRead] = Field(description="The risk level assigned to the event")

    source: Optional[EventSourceRead] = Field(description="The source of the event")

    status: EventStatusRead = Field(description="The status assigned to the event")

    tags: List[NodeTagRead] = Field(description="A list of tags added to the event")

    threat_actors: List[NodeThreatActorRead] = Field(description="A list of threat actors added to the event")

    threats: List[NodeThreatRead] = Field(description="A list of threats added to the event")

    type: Optional[EventTypeRead] = Field(description="The type assigned to the event")

    uuid: UUID4 = Field(description="The UUID of the event")

    vectors: List[EventVectorRead] = Field(description="A list of vectors assigned to the event")

    _convert_association_list: classmethod = validators.convert_association_list("alert_uuids")

    class Config:
        orm_mode = True


class EventUpdate(NodeUpdate, EventBase):
    history_username: Optional[type_str] = Field(
        description="If given, an event history record will be created and associated with the user"
    )

    name: Optional[type_str] = Field(description="The name of the event")

    queue: Optional[type_str] = Field(description="The event queue containing this event")

    status: Optional[type_str] = Field(description="The status assigned to the event")

    tags: Optional[List[type_str]] = Field(description="A list of tags to add to the event")

    threat_actors: Optional[List[type_str]] = Field(description="A list of threat actors to add to the event")

    threats: Optional[List[type_str]] = Field(description="A list of threats to add to the event")

    _prevent_none: classmethod = validators.prevent_none("name", "queue", "status", "tags", "threat_actors", "threats")


class EventUpdateMultiple(EventUpdate):
    uuid: UUID4 = Field(description="The UUID of the event")
