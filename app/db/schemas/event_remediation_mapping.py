from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


event_remediation_mapping = Table(
    "event_remediation_mapping",
    Base.metadata,
    Column(
        "event_uuid",
        UUID(as_uuid=True),
        ForeignKey("event.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "remediation_uuid",
        UUID(as_uuid=True),
        ForeignKey("event_remediation.uuid"),
        primary_key=True,
    ),
)
