from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


observable_tag_mapping = Table(
    "observable_tag_mapping",
    Base.metadata,
    Column(
        "observable_uuid",
        UUID(as_uuid=True),
        ForeignKey("observable.uuid"),
        index=True,
        primary_key=True,
    ),
    Column(
        "tag_uuid",
        UUID(as_uuid=True),
        ForeignKey("metadata_tag.uuid"),
        index=True,
        primary_key=True,
    ),
)
