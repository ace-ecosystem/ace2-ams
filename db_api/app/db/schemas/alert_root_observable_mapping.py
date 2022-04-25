from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


alert_root_observable_mapping = Table(
    "alert_root_observable_mapping",
    Base.metadata,
    Column(
        "alert_uuid",
        UUID(as_uuid=True),
        ForeignKey("alert.uuid", ondelete="CASCADE"),
        index=True,
        primary_key=True,
    ),
    Column(
        "observable_uuid",
        UUID(as_uuid=True),
        ForeignKey("observable.uuid"),
        index=True,
        primary_key=True,
    ),
)
