from sqlalchemy import Column, ForeignKey, func, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.format import Format


class AnalysisSummaryDetail(Base):
    __tablename__ = "analysis_summary_detail"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    analysis_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"), index=True, nullable=False)

    content = Column(String, nullable=False)

    format_uuid = Column(UUID(as_uuid=True), ForeignKey("format.uuid"), nullable=False)

    format: Format = relationship("Format", foreign_keys=[format_uuid], lazy="selectin")

    header = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("analysis_uuid", "header", "content", name="analysis_header_content_uc"),)
