from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


node_threat_mapping = Table(
    "node_threat_mapping",
    Base.metadata,
    Column(
        "node_uuid",
        UUID(as_uuid=True),
        ForeignKey("node.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "threat_uuid",
        UUID(as_uuid=True),
        ForeignKey("node_threat.uuid"),
        primary_key=True,
    ),
)
