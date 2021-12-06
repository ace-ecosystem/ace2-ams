from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


analysis_module_type_tag_mapping = Table(
    "analysis_module_type_tag_mapping",
    Base.metadata,
    Column(
        "analysis_module_type_uuid",
        UUID(as_uuid=True),
        ForeignKey("analysis_module_type.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "tag_uuid",
        UUID(as_uuid=True),
        ForeignKey("node_tag.uuid"),
        index=True,
        primary_key=True,
    ),
)
