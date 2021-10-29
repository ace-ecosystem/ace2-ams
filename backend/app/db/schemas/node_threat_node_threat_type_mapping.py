from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


node_threat_node_threat_type_mapping = Table(
    "node_threat_node_threat_type_mapping",
    Base.metadata,
    Column(
        "node_threat_uuid",
        UUID(as_uuid=True),
        ForeignKey("node_threat.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "node_threat_type_uuid",
        UUID(as_uuid=True),
        ForeignKey("node_threat_type.uuid"),
        primary_key=True,
    ),
)
