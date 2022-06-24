from sqlalchemy import Column, ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class ObservableRelationship(Base):
    __tablename__ = "observable_relationship"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), index=True)

    # The relationship is not loaded automatically
    observable = relationship("Observable", foreign_keys=[observable_uuid])

    related_observable_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"))

    related_observable = relationship("Observable", foreign_keys=[related_observable_uuid], lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_relationship_type.uuid"))

    type = relationship("ObservableRelationshipType", foreign_keys=[type_uuid], lazy="selectin")

    __table_args__ = (
        UniqueConstraint("observable_uuid", "related_observable_uuid", "type_uuid", name="observable_related_type_uc"),
    )
