from datetime import datetime
from pydantic import Field, StrictBool, UUID4
from typing import List, Optional
from uuid import uuid4

from api.models import type_str, validators
from api.models.node import NodeBase, NodeCreate, NodeRead, NodeTreeCreateWithNode, NodeTreeItemRead, NodeUpdate
from api.models.node_comment import NodeCommentRead
from api.models.node_detection_point import NodeDetectionPointRead
from api.models.node_directive import NodeDirectiveRead
from api.models.node_relationship import NodeRelationshipRead
from api.models.node_tag import NodeTagRead
from api.models.node_threat import NodeThreatRead
from api.models.node_threat_actor import NodeThreatActorRead
from api.models.observable_type import ObservableTypeRead


class ObservableBase(NodeBase):
    """Represents a unique observable (based on the type+value)."""

    context: Optional[type_str] = Field(
        description="""Optional context surrounding the observation. This is used to communicate additional information
            to the analysts, such as where the observation was made. For example, 'Source IP address of the sender of
            the email.' or 'From address in the email.'"""
    )

    expires_on: Optional[datetime] = Field(
        description="The time the observable will expire and no longer be included in observable detection exports"
    )

    for_detection: StrictBool = Field(
        default=False,
        description="Whether or not this observable should be included in the observable detection exports",
    )

    redirection_uuid: Optional[UUID4] = Field(
        description="The UUID of another observable to which this one should point"
    )

    time: datetime = Field(default_factory=datetime.utcnow, description="The time this observable was observed")

    type: type_str = Field(description="The type of the observable")

    value: type_str = Field(description="The value of the observable")


class ObservableCreateBase(NodeCreate, ObservableBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable")


class ObservableCreateWithAlert(ObservableCreateBase):
    pass


class ObservableCreate(ObservableCreateBase):
    directives: List[type_str] = Field(
        default_factory=list, description="A list of directives to add to the observable"
    )

    node_tree: NodeTreeCreateWithNode = Field(description="This defines where in a Node Tree this observable fits")

    tags: List[type_str] = Field(default_factory=list, description="A list of tags to add to the observable")

    threat_actors: List[type_str] = Field(
        default_factory=list, description="A list of threat actors to add to the observable"
    )

    threats: List[type_str] = Field(default_factory=list, description="A list of threats to add to the observable")


class ObservableRead(NodeRead, ObservableBase):
    comments: List[NodeCommentRead] = Field(
        description="A list of comments added to the observable", default_factory=list
    )

    detection_points: List[NodeDetectionPointRead] = Field(
        description="A list of detection points added to the observable", default_factory=list
    )

    directives: List[NodeDirectiveRead] = Field(description="A list of directives added to the observable")

    observable_relationships: List["ObservableRelationshipRead"] = Field(
        description="A list of observable relationships for this observable"
    )

    tags: List[NodeTagRead] = Field(description="A list of tags added to the observable")

    threat_actors: List[NodeThreatActorRead] = Field(description="A list of threat actors added to the observable")

    threats: List[NodeThreatRead] = Field(description="A list of threats added to the observable")

    type: ObservableTypeRead = Field(description="The type of the observable")

    uuid: UUID4 = Field(description="The UUID of the observable")

    class Config:
        orm_mode = True


class ObservableNodeTreeRead(ObservableRead, NodeTreeItemRead):
    """Model used to control which information for an Observable is displayed when getting an alert tree"""

    class Config:
        orm_mode = True


class ObservableUpdate(NodeUpdate, ObservableBase):
    directives: Optional[List[type_str]] = Field(description="A list of directives to add to the observable")

    for_detection: Optional[StrictBool] = Field(
        description="Whether or not this observable should be included in the observable detection exports"
    )

    tags: Optional[List[type_str]] = Field(description="A list of tags to add to the observable")

    threat_actors: Optional[List[type_str]] = Field(description="A list of threat actors to add to the observable")

    threats: Optional[List[type_str]] = Field(description="A list of threats to add to the observable")

    time: Optional[datetime] = Field(description="The time this observable was observed")

    type: Optional[type_str] = Field(description="The type of the observable")

    value: Optional[type_str] = Field(description="The value of the observable")

    _prevent_none: classmethod = validators.prevent_none(
        "directives", "for_detection", "tags", "threat_actors", "threats", "time", "type", "value"
    )


class ObservableRelationshipRead(NodeRelationshipRead):
    related_node: ObservableRead = Field(description="The related observable")


# This is needed for the circular relationship between ObservableRead and ObservableRelationshipRead
ObservableRead.update_forward_refs()
ObservableNodeTreeRead.update_forward_refs()
