import json

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
from typing import List

from api_models.observable import ObservableNodeTreeRead, ObservableRead, ObservableRelationshipRead
from db.database import Base
from db.schemas.helpers import utcnow
from db.schemas.history import HasHistory, HistoryMixin
from db.schemas.node import Node
from db.schemas.node_relationship import NodeRelationship


class ObservableHistory(Base, HistoryMixin):
    __tablename__ = "observable_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), index=True, nullable=False)


class Observable(Node, HasHistory):
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

    def convert_to_pydantic(self) -> ObservableNodeTreeRead:
        return ObservableNodeTreeRead(**self.to_dict())

    def to_dict(self):
        values_dict = self.__dict__
        values_dict["observable_relationships"] = self.observable_relationships
        return values_dict

    @property
    def history_snapshot(self):
        return json.loads(ObservableRead(**self.to_dict()).json())

    @property
    def observable_relationships(self) -> List[ObservableRelationshipRead]:
        """Returns the list of observable relationships for this observable sorted by the
        related observable's type then value"""

        results: List[NodeRelationship] = [r for r in self.relationships if isinstance(r.related_node, Observable)]

        return sorted(results, key=lambda x: (x.related_node.type.value, x.related_node.value))
