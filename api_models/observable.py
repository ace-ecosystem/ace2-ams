from datetime import datetime
from pydantic import BaseModel, Field, StrictBool, UUID4
from typing import Optional
from uuid import UUID, uuid4

from api_models import type_str, validators
from api_models.analysis_metadata import AnalysisMetadataCreate, AnalysisMetadataRead
from api_models.metadata_tag import MetadataTagRead
from api_models.node import NodeBase, NodeCreate, NodeRead, NodeUpdate
from api_models.node_comment import NodeCommentRead
from api_models.node_relationship import NodeRelationshipRead
from api_models.node_threat import NodeThreatRead
from api_models.node_threat_actor import NodeThreatActorRead
from api_models.observable_type import ObservableTypeRead


class DispositionHistoryIndividual(BaseModel):
    """Represents an individual disposition history."""

    disposition: type_str = Field(description="The disposition value")

    count: int = Field(description="The number of times the disposition occurred")

    percent: int = Field(description="The percent of times the disposition occurred")


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

    type: type_str = Field(description="The type of the observable")

    value: type_str = Field(description="The value of the observable")


class ObservableCreateBase(NodeCreate, ObservableBase):
    analyses: "list[AnalysisCreateInObservable]" = Field(
        default_factory=list, description="A list of analysis results to add as children to the observable"
    )

    analysis_metadata: list[AnalysisMetadataCreate] = Field(
        default_factory=list, description="A list of metadata objects to add to the observable by its parent analysis"
    )

    history_username: Optional[type_str] = Field(
        description="If given, an observable history record will be created and associated with the user"
    )

    observable_relationships: "list[ObservableRelationshipCreate]" = Field(
        default_factory=list, description="A list of observable relationships to add to this observable"
    )

    tags: list[type_str] = Field(default_factory=list, description="A list of tags to add to the observable")

    threat_actors: list[type_str] = Field(
        default_factory=list, description="A list of threat actors to add to the observable"
    )

    threats: list[type_str] = Field(default_factory=list, description="A list of threats to add to the observable")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable")


class ObservableCreate(ObservableCreateBase):
    parent_analysis_uuid: Optional[UUID] = Field(
        description="The UUID of the analysis that will contain this observable. This can be NULL if you pass in an Analysis object when creating an observable."
    )


class ObservableCreateInSubmission(ObservableCreateBase):
    pass


class ObservableRead(NodeRead, ObservableBase):
    comments: list[NodeCommentRead] = Field(
        description="A list of comments added to the observable", default_factory=list
    )

    # Set a static string value so code displaying the tree structure knows which type of object this is.
    object_type: str = "observable"

    observable_relationships: "list[ObservableRelationshipRead]" = Field(
        description="A list of observable relationships for this observable"
    )

    tags: list[MetadataTagRead] = Field(description="A list of tags added to the observable")

    threat_actors: list[NodeThreatActorRead] = Field(description="A list of threat actors added to the observable")

    threats: list[NodeThreatRead] = Field(description="A list of threats added to the observable")

    type: ObservableTypeRead = Field(description="The type of the observable")

    uuid: UUID4 = Field(description="The UUID of the observable")

    class Config:
        orm_mode = True


class ObservableSubmissionRead(ObservableRead):
    """Model used to control which information for an Observable is displayed when getting Observables contained in a list of Submissions."""

    analysis_metadata: AnalysisMetadataRead = Field(description="The analysis metadata for the observable")

    disposition_history: list[DispositionHistoryIndividual] = Field(
        default_factory=list,
        description="A list of the dispositions and their counts of alerts that contain this observable",
    )

    class Config:
        orm_mode = True


class ObservableSubmissionTreeRead(ObservableSubmissionRead):
    """Model used to control which information for an Observable is displayed when getting a submission tree"""

    children: "list[AnalysisSubmissionTreeRead]" = Field(
        default_factory=list, description="A list of this observable's child analysis"
    )

    first_appearance: bool = Field(
        default=True, description="Whether or not this is the first time the object appears in the tree"
    )

    class Config:
        orm_mode = True


class ObservableUpdate(NodeUpdate, ObservableBase):
    for_detection: Optional[StrictBool] = Field(
        description="Whether or not this observable should be included in the observable detection exports"
    )

    history_username: Optional[type_str] = Field(
        description="If given, an observable history record will be created and associated with the user"
    )

    tags: Optional[list[type_str]] = Field(description="A list of tags to add to the observable")

    threat_actors: Optional[list[type_str]] = Field(description="A list of threat actors to add to the observable")

    threats: Optional[list[type_str]] = Field(description="A list of threats to add to the observable")

    type: Optional[type_str] = Field(description="The type of the observable")

    value: Optional[type_str] = Field(description="The value of the observable")

    _prevent_none: classmethod = validators.prevent_none(
        "for_detection", "tags", "threat_actors", "threats", "time", "type", "value"
    )


class ObservableRelationshipCreate(BaseModel):
    relationship_type: type_str = Field(description="The type of the observable relationship")

    type: type_str = Field(description="The related observable's type")

    value: type_str = Field(description="The related observable's value")


class ObservableRelationshipRead(NodeRelationshipRead):
    related_node: ObservableRead = Field(description="The related observable")


# This is needed for the circular relationship between ObservableRead and ObservableRelationshipRead
# and ObservableCreate <-> AnalysisCreateInObservable.
from api_models.analysis import AnalysisCreateInObservable, AnalysisSubmissionTreeRead

ObservableCreate.update_forward_refs()
ObservableCreateInSubmission.update_forward_refs()
ObservableSubmissionRead.update_forward_refs()
ObservableSubmissionTreeRead.update_forward_refs()
ObservableRead.update_forward_refs()
