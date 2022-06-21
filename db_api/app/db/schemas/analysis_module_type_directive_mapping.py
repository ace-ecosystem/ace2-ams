from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


analysis_module_type_directive_mapping = Table(
    "analysis_module_type_directive_mapping",
    Base.metadata,
    Column(
        "analysis_module_type_uuid",
        UUID(as_uuid=True),
        ForeignKey("analysis_module_type.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "directive_uuid",
        UUID(as_uuid=True),
        ForeignKey("metadata_directive.uuid"),
        index=True,
        primary_key=True,
    ),
)
