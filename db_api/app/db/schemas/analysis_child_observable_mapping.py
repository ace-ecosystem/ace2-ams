from sqlalchemy import Column, ForeignKey, func, Index
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


class AnalysisChildObservableMapping(Base):
    __tablename__ = "analysis_child_observable_mapping"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    analysis_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"), nullable=False, index=True)

    child_observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), nullable=False, index=True)

    metadata_uuid = Column(UUID(as_uuid=True), ForeignKey("metadata.uuid"), nullable=True)

    # These two partial indices combine to enforce the uniqueness of analysis_uuid + child_observable_uuid + metadata_uuid
    # even when the metadata_uuid is NULL. This is so that you cannot create the same entry twice.
    __table_args__ = (
        Index(
            "uix_analysis_child_observable_metadata",
            "analysis_uuid",
            "child_observable_uuid",
            "metadata_uuid",
            unique=True,
            postgresql_where=metadata_uuid.isnot(None),
        ),
        Index(
            "uix_analysis_child_observable",
            "analysis_uuid",
            "child_observable_uuid",
            unique=True,
            postgresql_where=metadata_uuid.is_(None),
        ),
    )
