from datetime import datetime
from pydantic import BaseModel, Field, StrictBool, UUID4
from typing import Optional
from uuid import UUID, uuid4

from api_models import type_str, validators
from api_models.analysis_metadata import AnalysisMetadataCreate, AnalysisMetadataRead
from api_models.metadata_tag import MetadataTagRead
from api_models.observable_type import ObservableTypeRead


class ObservableDispositionHistoryIndividual(BaseModel):
    """Represents an individual disposition history."""

    disposition: type_str = Field(description="The disposition value")

    count: int = Field(
        description="The number of times the disposition occurred")

    percent: int = Field(
        description="The percent of times the disposition occurred")


class ObservableMatchingEventIndividual(BaseModel):
    """Represents an individual matching event that contains this observable."""

    status: type_str = Field(description="The status of the matching event")

    count: int = Field(
        description="The number of events with this status that contain the observable")


class ObservableBase(BaseModel):
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

    version: UUID4 = Field(
        default_factory=uuid4,
        description="""A version string that automatically changes every time the observable is modified.""",
    )

    whitelisted: StrictBool = Field(
        default=False,
        description="Whether or not this observable is whitelisted. Whitelisted means no analysis will be performed on it.",
    )


class ObservableCreateBase(ObservableBase):
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

    tags: list[type_str] = Field(
        default_factory=list, description="A list of tags to add to the observable")

    uuid: UUID4 = Field(default_factory=uuid4,
                        description="The UUID of the observable")


class ObservableCreate(ObservableCreateBase):
    parent_analysis_uuid: Optional[UUID] = Field(
        description="The UUID of the analysis that will contain this observable. This can be NULL if you pass in an Analysis object when creating an observable."
    )


class ObservableCreateInSubmission(ObservableCreateBase):
    pass


class ObservableRead(ObservableBase):
    # Set a static string value so code displaying the tree structure knows which type of object this is.
    object_type: str = "observable"

    observable_relationships: "list[ObservableRelationshipRead]" = Field(
        description="A list of observable relationships for this observable"
    )

    tags: list[MetadataTagRead] = Field(
        description="A list of tags added to the observable")

    type: ObservableTypeRead = Field(description="The type of the observable")

    uuid: UUID4 = Field(description="The UUID of the observable")

    class Config:
        orm_mode = True


class ObservableSubmissionRead(ObservableRead):
    """Model used to control which information for an Observable is displayed when getting Observables contained in a list of Submissions."""

    analysis_metadata: AnalysisMetadataRead = Field(
        description="The analysis metadata for the observable")

    disposition_history: list[ObservableDispositionHistoryIndividual] = Field(
        default_factory=list,
        description="A list of the dispositions and their counts of alerts that contain this observable",
    )

    matching_events: list[ObservableMatchingEventIndividual] = Field(
        default_factory=list,
        description="A list of the event statuses and their counts of events that contain this observable",
    )

    class Config:
        orm_mode = True


class ObservableSubmissionTreeRead(ObservableSubmissionRead):
    """Model used to control which information for an Observable is displayed when getting a submission tree"""

    children: "list[AnalysisSubmissionTreeRead]" = Field(
        default_factory=list, description="A list of this observable's child analysis"
    )

    critical_path: bool = Field(
        default=False, description="Whether or not this object is part of a 'critical' path in the tree"
    )

    jump_to_leaf: Optional[type_str] = Field(
        description="The identifier of the first occurrence of this observable in the tree where the analysis can be viewed"
    )

    leaf_id: type_str = Field(
        description="The unique identifier of the observable in the nested tree structure")

    class Config:
        orm_mode = True


class ObservableUpdate(ObservableBase):
    for_detection: Optional[StrictBool] = Field(
        description="Whether or not this observable should be included in the observable detection exports"
    )

    history_username: Optional[type_str] = Field(
        description="If given, an observable history record will be created and associated with the user"
    )

    tags: Optional[list[type_str]] = Field(
        description="A list of tags to add to the observable")

    type: Optional[type_str] = Field(description="The type of the observable")

    value: Optional[type_str] = Field(
        description="The value of the observable")

    # The version is optional when updating an observable since certain actions in the GUI do not need to care
    # about the version. However, if the version is given, the update will be rejected if it does not match.
    version: Optional[UUID4] = Field(
        description="""A version string that automatically changes every time the observable is modified. If supplied,
        the version must match when updating.""",
    )

    _prevent_none: classmethod = validators.prevent_none(
        "for_detection", "tags", "time", "type", "value")


class ObservableRelationshipCreate(BaseModel):
    relationship_type: type_str = Field(
        description="The type of the observable relationship")

    type: type_str = Field(description="The related observable's type")

    value: type_str = Field(description="The related observable's value")


class ObservableVersion(BaseModel):
    version: UUID4 = Field(description="The current version of the observable")

    class Config:
        orm_mode = True


# This is needed for the circular relationship between ObservableRead and ObservableRelationshipRead
# and ObservableCreate <-> AnalysisCreateInObservable.
from api_models.analysis import AnalysisCreateInObservable, AnalysisSubmissionTreeRead
from api_models.observable_relationship import ObservableRelationshipRead

ObservableCreate.update_forward_refs()
ObservableCreateInSubmission.update_forward_refs()
ObservableSubmissionRead.update_forward_refs()
ObservableSubmissionTreeRead.update_forward_refs()
ObservableRead.update_forward_refs()
