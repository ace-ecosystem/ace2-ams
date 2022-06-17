from datetime import datetime
from pydantic import BaseModel, Field, UUID4
from typing import Optional, Union

from api_models import type_str
from api_models.metadata_directive import MetadataDirectiveRead
from api_models.metadata_display_type import MetadataDisplayTypeRead
from api_models.metadata_display_value import MetadataDisplayValueRead
from api_models.metadata_tag import MetadataTagRead
from api_models.metadata_time import MetadataTimeRead


class AnalysisMetadataCreate(BaseModel):
    """Represents a metadata object that was added to an observable by the analysis."""

    analysis_uuid: Optional[UUID4] = Field(
        description="The UUID of the analysis that added this metadata. This can be NULL if you pass in an Analysis object when creating the metadata."
    )

    observable_uuid: Optional[UUID4] = Field(
        description="The UUID of the observable to which this metadata was added. This can be NULL if you pass in an Observable object when creating the metadata."
    )

    type: type_str = Field(description="The type of the metadata")

    value: Union[type_str, datetime] = Field(description="The value of the metadata")


class AnalysisMetadataRead(BaseModel):
    """Represents the collection of analysis metadata that was added to an observable."""

    directives: list[MetadataDirectiveRead] = Field(
        default_factory=list, description="A list of directives added to the observable"
    )

    display_type: Optional[MetadataDisplayTypeRead] = Field(description="The display type of the observable")

    display_value: Optional[MetadataDisplayValueRead] = Field(description="The display value of the observable")

    tags: list[MetadataTagRead] = Field(default_factory=list, description="A list of tags added to the observable")

    time: Optional[MetadataTimeRead] = Field(description="The time added to the observable")
