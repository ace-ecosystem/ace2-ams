from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators
from api_models.format import FormatRead


class AnalysisSummaryDetailCreateBase(BaseModel):
    content: type_str = Field(description="The content of the analysis summary detail")

    format: type_str = Field(description="The format to use when displaying in the GUI")

    header: type_str = Field(description="The header or title of the analysis summary detail")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the analysis summary detail")


class AnalysisSummaryDetailCreate(AnalysisSummaryDetailCreateBase):
    analysis_uuid: UUID4 = Field(description="The analysis UUID that should receive this summary detail")


class AnalysisSummaryDetailCreateInAnalysis(AnalysisSummaryDetailCreateBase):
    pass


class AnalysisSummaryDetailRead(BaseModel):
    uuid: UUID4 = Field(description="The UUID of the analysis summary detail")

    content: type_str = Field(description="The content of the analysis summary detail")

    format: FormatRead = Field(description="The format to use when displaying in the GUI")

    header: type_str = Field(description="The header or title of the analysis summary detail")

    class Config:
        orm_mode = True


class AnalysisSummaryDetailUpdate(BaseModel):
    content: Optional[type_str] = Field(description="The content of the analysis summary detail")

    format: Optional[type_str] = Field(description="The format to use when displaying in the GUI")

    header: Optional[type_str] = Field(description="The header or title of the analysis summary detail")

    _prevent_none: classmethod = validators.prevent_none("content", "format", "header")
