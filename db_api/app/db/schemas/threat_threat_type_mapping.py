from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


threat_threat_type_mapping = Table(
    "threat_threat_type_mapping",
    Base.metadata,
    Column(
        "threat_uuid",
        UUID(as_uuid=True),
        ForeignKey("threat.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "threat_type_uuid",
        UUID(as_uuid=True),
        ForeignKey("threat_type.uuid"),
        index=True,
        primary_key=True,
    ),
)
