from pydantic import BaseModel, Field, Json, StrictBool, StrictInt, UUID4
from typing import List, Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.node_directive import NodeDirectiveRead
from api_models.node_tag import NodeTagRead
from api_models.observable_type import ObservableTypeRead


class AnalysisModuleTypeBase(BaseModel):
    """Represents a type of analysis module registered with the core."""

    cache_seconds: StrictInt = Field(
        description="The number of seconds that analysis produced by this module is cached"
    )

    description: Optional[type_str] = Field(
        description="An optional human-readable description of the analysis module type"
    )

    extended_version: Optional[Json] = Field(
        description="""An optional dictionary of arbitrary key/value pairs that
        can be used to add additional version data to the module. Analysis
        modules that use some kind of external data can use these fields to
        include the version of the data that was used at the time of analysis."""
    )

    manual: StrictBool = Field(
        default=False,
        description="Whether or not this analysis module type runs in manual mode.",
    )

    observable_types: List[type_str] = Field(
        default_factory=list,
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types.""",
    )

    required_directives: List[type_str] = Field(
        default_factory=list,
        description="""A list of directives an observable must have in order to be analyzed by this module. An empty
        list means that no directives are required.""",
    )

    required_tags: List[type_str] = Field(
        default_factory=list,
        description="""A list of tags an observable must have in order to be analyzed by this module. An empty list
        means that no tags are required.""",
    )

    value: type_str = Field(description="The value of the analysis module type")

    version: type_str = Field(description="Version number of the analysis module type in SemVer format (ex: 1.0.0)")

    _validate_version: classmethod = validators.version("version")


class AnalysisModuleTypeCreate(AnalysisModuleTypeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the analysis module type")


class AnalysisModuleTypeNodeTreeRead(BaseModel):
    """Model used to control which information for an AnalysisModuleType is displayed when getting an alert tree"""

    value: type_str = Field(description="The value of the analysis module type")

    uuid: UUID4 = Field(description="The UUID of the analysis module type")

    class Config:
        orm_mode = True


class AnalysisModuleTypeRead(AnalysisModuleTypeBase):
    extended_version: Optional[dict] = Field(
        description="""An optional dictionary of arbitrary key/value pairs that
        can be used to add additional version data to the module. Analysis
        modules that use some kind of external data can use these fields to
        include the version of the data that was used at the time of analysis."""
    )

    observable_types: List[ObservableTypeRead] = Field(
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types."""
    )

    required_directives: List[NodeDirectiveRead] = Field(
        description="""A list of directives an observable must have in order to be analyzed by this module. An empty
        list means that no directives are required.""",
    )

    required_tags: List[NodeTagRead] = Field(
        description="""A list of tags an observable must have in order to be analyzed by this module. An empty list
        means that no tags are required.""",
    )

    uuid: UUID4 = Field(description="The UUID of the analysis module type")

    class Config:
        orm_mode = True


class AnalysisModuleTypeUpdate(AnalysisModuleTypeBase):
    cache_seconds: Optional[StrictInt] = Field(
        description="The number of seconds that analysis produced by this module is cached"
    )

    manual: Optional[StrictBool] = Field(description="Whether or not this analysis module type runs in manual mode.")

    observable_types: Optional[List[type_str]] = Field(
        description="""A list of observable types this analysis module type knows how to analyze.
        An empty list means it supports ALL observable types.""",
    )

    required_directives: Optional[List[type_str]] = Field(
        description="""A list of directives an observable must have in order to be analyzed by this module. An empty
        list means that no directives are required.""",
    )

    required_tags: Optional[List[type_str]] = Field(
        description="""A list of tags an observable must have in order to be analyzed by this module. An empty list
        means that no tags are required.""",
    )

    value: Optional[type_str] = Field(description="The value of the analysis module type")

    version: Optional[type_str] = Field(
        description="Version number of the analysis module type in SemVer format (ex: 1.0.0)"
    )

    _prevent_none: classmethod = validators.prevent_none(
        "cache_seconds",
        "manual",
        "observable_types",
        "required_directives",
        "required_tags",
        "value",
    )
