from sqlalchemy import func, Boolean, Column, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.analysis_module_type_directive_mapping import analysis_module_type_directive_mapping
from db.schemas.analysis_module_type_observable_type_mapping import analysis_module_type_observable_type_mapping
from db.schemas.analysis_module_type_tag_mapping import analysis_module_type_tag_mapping


class AnalysisModuleType(Base):
    __tablename__ = "analysis_module_type"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    cache_seconds = Column(Integer, nullable=False)

    description = Column(String)

    extended_version = Column(JSONB)

    manual = Column(Boolean, default=False, nullable=False)

    observable_types = relationship(
        "ObservableType",
        secondary=analysis_module_type_observable_type_mapping,
        passive_deletes=True,
    )

    required_directives = relationship(
        "MetadataDirective",
        secondary=analysis_module_type_directive_mapping,
        passive_deletes=True,
    )

    required_tags = relationship(
        "MetadataTag",
        secondary=analysis_module_type_tag_mapping,
        passive_deletes=True,
    )

    value = Column(String, nullable=False, index=True)

    version = Column(String, nullable=False, index=True)

    __table_args__ = (
        Index("value_version", value, version),
        Index(
            "amt_value_trgm",
            value,
            postgresql_ops={"value": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
        UniqueConstraint("value", "version", name="value_version_uc"),
    )
