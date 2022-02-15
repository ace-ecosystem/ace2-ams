from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.models.observable import ObservableNodeTreeRead
from db.database import Base
from db.schemas.helpers import utcnow
from db.schemas.history import HistoryMixin
from db.schemas.node import Node


class ObservableHistory(Base, HistoryMixin):
    __tablename__ = "observable_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), index=True, nullable=False)


class Observable(Node):
    __tablename__ = "observable"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    context = Column(String)

    # Using timezone=True causes PostgreSQL to store the datetime as UTC. Datetimes without timezone
    # information will be assumed to be UTC, whereas datetimes with timezone data will be converted to UTC.
    expires_on = Column(DateTime(timezone=True))

    for_detection = Column(Boolean, default=False, nullable=False)

    # History is lazy loaded and is not included by default when fetching an observable from the API.
    history = relationship(
        "ObservableHistory",
        primaryjoin="ObservableHistory.record_uuid == Observable.uuid",
        order_by="ObservableHistory.action_time",
    )

    redirection_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"))

    redirection = relationship("Observable", foreign_keys=[redirection_uuid], uselist=False)

    time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    type = relationship("ObservableType", lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_type.uuid"), nullable=False)

    value = Column(String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": "observable", "polymorphic_load": "inline"}

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

    def serialize_for_node_tree(self) -> ObservableNodeTreeRead:
        return ObservableNodeTreeRead(**self.__dict__)
