from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


analysis_observable_instance_mapping = Table(
    "analysis_observable_instance_mapping",
    Base.metadata,
    Column(
        "analysis_uuid",
        UUID(as_uuid=True),
        ForeignKey("analysis.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "observable_instance_uuid",
        UUID(as_uuid=True),
        ForeignKey("observable_instance.uuid"),
        index=True,
        primary_key=True,
        unique=True,
    ),
)
