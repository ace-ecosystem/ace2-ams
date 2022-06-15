from pydantic import BaseModel, Field, UUID4
from typing import Optional

from api_models import type_str


class AnalysisMetadataCreate(BaseModel):
    """Represents a metadata object that was added to an observable by the analysis."""

    analysis_uuid: Optional[UUID4] = Field(
        description="The UUID of the analysis that added this metadata. This can be NULL if you pass in an Analysis object when creating the metadata."
    )

    observable_uuid: Optional[UUID4] = Field(
        description="The UUID of the observable to which this metadata was added. This can be NULL if you pass in an Observable object when creating the metadata."
    )

    type: type_str = Field(description="The type of the metadata")

    value: type_str = Field(description="The value of the metadata")
