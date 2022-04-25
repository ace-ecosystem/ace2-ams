from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class AnalysisObservableMetadata(Base):
    __tablename__ = "analysis_observable_metadata"

    analysis_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"), primary_key=True, index=True)

    observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), primary_key=True, index=True)

    metadata_uuid = Column(UUID(as_uuid=True), ForeignKey("metadata.uuid"), primary_key=True)

    metadata = relationship("Metadata", foreign_keys=[metadata_uuid], lazy="selectin")
