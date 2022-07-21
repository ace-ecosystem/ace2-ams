from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


submission_tag_mapping = Table(
    "submission_tag_mapping",
    Base.metadata,
    Column(
        "submission_uuid",
        UUID(as_uuid=True),
        ForeignKey("submission.uuid"),
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
