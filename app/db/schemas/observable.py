from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    func,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class Observable(Base):
    __tablename__ = "observable"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    # Using timezone=True causes PostgreSQL to store the datetime as UTC. Datetimes without timezone
    # information will be assumed to be UTC, whereas datetimes with timezone data will be converted to UTC.
    expires_on = Column(DateTime(timezone=True))

    for_detection = Column(Boolean, default=False, nullable=False)

    type = relationship("ObservableType")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_type.uuid"), nullable=False)

    value = Column(String, nullable=False)

    __table_args__ = (
        Index(
            "observable_value_trgm",
            value,
            postgresql_ops={"value": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
        Index("type_value", type_uuid, value),
        UniqueConstraint("type_uuid", "value", name="type_value_uc"),
    )
