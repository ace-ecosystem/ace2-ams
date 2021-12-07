from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


node_directive_mapping = Table(
    "node_directive_mapping",
    Base.metadata,
    Column(
        "node_uuid",
        UUID(as_uuid=True),
        ForeignKey("node.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "directive_uuid",
        UUID(as_uuid=True),
        ForeignKey("node_directive.uuid"),
        index=True,
        primary_key=True,
    ),
)
