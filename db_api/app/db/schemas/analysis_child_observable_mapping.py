from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


analysis_child_observable_mapping = Table(
    "analysis_child_observable_mapping",
    Base.metadata,
    Column(
        "analysis_uuid",
        UUID(as_uuid=True),
        ForeignKey("analysis.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "observable_uuid",
        UUID(as_uuid=True),
        ForeignKey("observable.uuid"),
        index=True,
        primary_key=True,
    ),
)
