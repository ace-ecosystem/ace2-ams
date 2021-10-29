from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


observable_instance_analysis_mapping = Table(
    "observable_instance_analysis_mapping",
    Base.metadata,
    Column(
        "observable_instance_uuid",
        UUID(as_uuid=True),
        ForeignKey("observable_instance.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "analysis_uuid",
        UUID(as_uuid=True),
        ForeignKey("analysis.uuid"),
        index=True,
        primary_key=True,
        unique=True,
    ),
)
