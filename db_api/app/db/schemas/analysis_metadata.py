from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.metadata import Metadata


class AnalysisMetadata(Base):
    __tablename__ = "analysis_metadata"

    analysis_uuid = Column(
        UUID(as_uuid=True), ForeignKey("analysis.uuid", ondelete="CASCADE"), index=True, primary_key=True
    )

    observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), primary_key=True)

    metadata_uuid = Column(UUID(as_uuid=True), ForeignKey("metadata.uuid"), primary_key=True)

    # The name "metadata" is used by SQLAlchemy, hence the name "metadata_object"
    metadata_object: Metadata = relationship("Metadata", lazy="selectin")
