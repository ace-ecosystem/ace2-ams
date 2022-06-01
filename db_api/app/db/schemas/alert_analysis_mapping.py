from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


alert_analysis_mapping = Table(
    "alert_analysis_mapping",
    Base.metadata,
    Column(
        "alert_uuid",
        UUID(as_uuid=True),
        ForeignKey("alert.uuid", ondelete="CASCADE"),
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
