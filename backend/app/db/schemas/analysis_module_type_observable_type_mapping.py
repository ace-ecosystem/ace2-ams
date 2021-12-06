from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


analysis_module_type_observable_type_mapping = Table(
    "analysis_module_type_observable_type_mapping",
    Base.metadata,
    Column(
        "analysis_module_type_uuid",
        UUID(as_uuid=True),
        ForeignKey("analysis_module_type.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "observable_type_uuid",
        UUID(as_uuid=True),
        ForeignKey("observable_type.uuid"),
        index=True,
        primary_key=True,
    ),
)
