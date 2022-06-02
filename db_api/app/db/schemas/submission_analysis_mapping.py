from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


submission_analysis_mapping = Table(
    "submission_analysis_mapping",
    Base.metadata,
    Column(
        "submission_uuid",
        UUID(as_uuid=True),
        ForeignKey("submission.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "analysis_uuid",
        UUID(as_uuid=True),
        ForeignKey("analysis.uuid"),
        index=True,
        primary_key=True,
    ),
)
