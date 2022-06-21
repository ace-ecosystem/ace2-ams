from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from db.schemas.metadata import Metadata


class MetadataDisplayType(Metadata):
    __tablename__ = "metadata_display_type"

    uuid = Column(UUID(as_uuid=True), ForeignKey("metadata.uuid"), primary_key=True)

    description = Column(String)

    value = Column(String, nullable=False, unique=True, index=True)

    __mapper_args__ = {"polymorphic_identity": "display_type", "polymorphic_load": "inline"}
