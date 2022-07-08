from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from db.schemas.metadata import Metadata


class MetadataSort(Metadata):
    __tablename__ = "metadata_sort"

    uuid = Column(UUID(as_uuid=True), ForeignKey("metadata.uuid"), primary_key=True)

    description = Column(String)

    value = Column(Integer, nullable=False, unique=True, index=True)

    __mapper_args__ = {"polymorphic_identity": "sort", "polymorphic_load": "inline"}
