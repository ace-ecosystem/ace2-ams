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

from api_models.observable import ObservableSubmissionTreeRead, ObservableRead, ObservableRelationshipRead
from db.database import Base
from db.schemas.helpers import utcnow
from db.schemas.history import HasHistory, HistoryMixin
from db.schemas.metadata_tag import MetadataTag
from db.schemas.node import Node
from db.schemas.node_relationship import NodeRelationship
from db.schemas.observable_permanent_tag_mapping import observable_permanent_tag_mapping


class ObservableHistory(Base, HistoryMixin):
    __tablename__ = "observable_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), index=True, nullable=False)


class Observable(Node, HasHistory):
    __tablename__ = "observable"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    # This is an empty list that gets populated by certain submission-related queries.
    analysis_tags: list[MetadataTag] = []

    context = Column(String)

    # Using timezone=True causes PostgreSQL to store the datetime as UTC. Datetimes without timezone
    # information will be assumed to be UTC, whereas datetimes with timezone data will be converted to UTC.
    expires_on = Column(DateTime(timezone=True))

    for_detection = Column(Boolean, default=False, nullable=False, index=True)

    # History is lazy loaded and is not included by default when fetching an observable from the API.
    history = relationship(
        "ObservableHistory",
        primaryjoin="ObservableHistory.record_uuid == Observable.uuid",
        order_by="ObservableHistory.action_time",
    )

    permanent_tags: list[MetadataTag] = relationship(
        "MetadataTag", secondary=observable_permanent_tag_mapping, lazy="selectin"
    )

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

    def convert_to_pydantic(self) -> ObservableSubmissionTreeRead:
        return ObservableSubmissionTreeRead(**self.to_dict())

    def to_dict(self):
        ignore_keys = ["convert_to_pydantic", "history", "history_snapshot", "to_dict"]
        return {key: getattr(self, key) for key in self.__class__.__dict__ if key not in ignore_keys}

    @property
    def history_snapshot(self):
        return json.loads(ObservableRead(**self.to_dict()).json())

    @property
    def observable_relationships(self) -> list[ObservableRelationshipRead]:
        """Returns the list of observable relationships for this observable sorted by the
        related observable's type then value"""

        results: list[NodeRelationship] = [r for r in self.relationships if isinstance(r.related_node, Observable)]

        return sorted(results, key=lambda x: (x.related_node.type.value, x.related_node.value))
