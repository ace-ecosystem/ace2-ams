from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from db.schemas.metadata import Metadata


class MetadataTime(Metadata):
    __tablename__ = "metadata_time"

    uuid = Column(UUID(as_uuid=True), ForeignKey("metadata.uuid"), primary_key=True)

    description = Column(String)

    value = Column(DateTime(timezone=True), nullable=False, unique=True, index=True)

    __mapper_args__ = {"polymorphic_identity": "time", "polymorphic_load": "inline"}
