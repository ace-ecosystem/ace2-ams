from datetime import datetime
from pydantic import Field, StrictBool, UUID4
from typing import Optional
from uuid import UUID, uuid4

from api_models import type_str, validators
from api_models.node import NodeBase, NodeCreate, NodeRead, NodeTreeItemRead, NodeUpdate
from api_models.node_comment import NodeCommentRead
from api_models.node_detection_point import NodeDetectionPointRead
from api_models.node_directive import NodeDirectiveRead
from api_models.node_relationship import NodeRelationshipRead
from api_models.node_tag import NodeTagRead
from api_models.node_threat import NodeThreatRead
from api_models.node_threat_actor import NodeThreatActorRead
from api_models.observable_type import ObservableTypeRead


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

    time: datetime = Field(default_factory=datetime.utcnow, description="The time this observable was observed")

    type: type_str = Field(description="The type of the observable")

    value: type_str = Field(description="The value of the observable")


class ObservableCreate(NodeCreate, ObservableBase):
    analyses: "list[AnalysisCreate]" = Field(
        default_factory=list, description="A list of analysis results to add as children to the observable"
    )

    directives: list[type_str] = Field(
        default_factory=list, description="A list of directives to add to the observable"
    )

    history_username: Optional[type_str] = Field(
        description="If given, an observable history record will be created and associated with the user"
    )

    parent_analysis_uuid: Optional[UUID] = Field(
        description="The UUID of the analysis that will contain this observable. This can be NULL if you pass in an Analysis object when creating an observable."
    )

    redirection: "Optional[ObservableCreate]" = Field(description="Another observable to which this one should point")

    tags: list[type_str] = Field(default_factory=list, description="A list of tags to add to the observable")

    threat_actors: list[type_str] = Field(
        default_factory=list, description="A list of threat actors to add to the observable"
    )

    threats: list[type_str] = Field(default_factory=list, description="A list of threats to add to the observable")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable")


class ObservableRead(NodeRead, ObservableBase):
    comments: list[NodeCommentRead] = Field(
        description="A list of comments added to the observable", default_factory=list
    )

    detection_points: list[NodeDetectionPointRead] = Field(
        description="A list of detection points added to the observable", default_factory=list
    )

    directives: list[NodeDirectiveRead] = Field(description="A list of directives added to the observable")

    observable_relationships: "list[ObservableRelationshipRead]" = Field(
        description="A list of observable relationships for this observable"
    )

    redirection: "Optional[ObservableRead]" = Field(description="Another observable to which this one points")

    tags: list[NodeTagRead] = Field(description="A list of tags added to the observable")

    threat_actors: list[NodeThreatActorRead] = Field(description="A list of threat actors added to the observable")

    threats: list[NodeThreatRead] = Field(description="A list of threats added to the observable")

    type: ObservableTypeRead = Field(description="The type of the observable")

    uuid: UUID4 = Field(description="The UUID of the observable")

    class Config:
        orm_mode = True


class ObservableNodeTreeRead(ObservableRead, NodeTreeItemRead):
    """Model used to control which information for an Observable is displayed when getting an alert tree"""

    class Config:
        orm_mode = True


class ObservableUpdate(NodeUpdate, ObservableBase):
    directives: Optional[list[type_str]] = Field(description="A list of directives to add to the observable")

    for_detection: Optional[StrictBool] = Field(
        description="Whether or not this observable should be included in the observable detection exports"
    )

    history_username: Optional[type_str] = Field(
        description="If given, an observable history record will be created and associated with the user"
    )

    redirection_uuid: Optional[UUID] = Field(description="The observable UUID to which the observable should redirect")

    tags: Optional[list[type_str]] = Field(description="A list of tags to add to the observable")

    threat_actors: Optional[list[type_str]] = Field(description="A list of threat actors to add to the observable")

    threats: Optional[list[type_str]] = Field(description="A list of threats to add to the observable")

    time: Optional[datetime] = Field(description="The time this observable was observed")

    type: Optional[type_str] = Field(description="The type of the observable")

    value: Optional[type_str] = Field(description="The value of the observable")

    _prevent_none: classmethod = validators.prevent_none(
        "directives", "for_detection", "tags", "threat_actors", "threats", "time", "type", "value"
    )


class ObservableRelationshipRead(NodeRelationshipRead):
    related_node: ObservableRead = Field(description="The related observable")


# This is needed for the circular relationship between ObservableRead and ObservableRelationshipRead
# and ObservableCreate <-> AnalysisCreate.
from api_models.analysis import AnalysisCreate

ObservableCreate.update_forward_refs()
ObservableRead.update_forward_refs()
ObservableNodeTreeRead.update_forward_refs()
