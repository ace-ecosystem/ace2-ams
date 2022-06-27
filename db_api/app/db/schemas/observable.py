import json

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
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from typing import Optional

from api_models.observable import ObservableSubmissionTreeRead, ObservableRead, ObservableRelationshipRead
from db.database import Base
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.analysis_metadata import AnalysisMetadata
from db.schemas.event_status import EventStatus
from db.schemas.history import HasHistory, HistoryMixin
from db.schemas.metadata_tag import MetadataTag
from db.schemas.observable_tag_mapping import observable_tag_mapping


class ObservableHistory(Base, HistoryMixin):
    __tablename__ = "observable_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("observable.uuid"), index=True, nullable=False)


class Observable(Base, HasHistory):
    __tablename__ = "observable"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    # NOTE: You could alter this relationship to directly return a list of AlertDisposition objects. However,
    # a SQLAlchemy relationship only returns unique/distinct objects. So if an observable appears in multiple alerts
    # that have the same disposition, you will only receive a single instance of that disposition in the relationship.
    #
    # Instead, the relationship is set up to return a list of alerts, and then an association proxy is used
    # to get a list of the alerts' dispositions.
    alerts = relationship(
        "Submission",
        secondary="join(Submission, submission_analysis_mapping, and_(Submission.alert == True, submission_analysis_mapping.c.submission_uuid == Submission.uuid))."
        "join(analysis_child_observable_mapping, analysis_child_observable_mapping.c.analysis_uuid == submission_analysis_mapping.c.analysis_uuid)",
        primaryjoin="Observable.uuid == analysis_child_observable_mapping.c.observable_uuid",
        viewonly=True,
        lazy="selectin",
    )

    alert_dispositions: list[AlertDisposition] = association_proxy("alerts", "disposition")

    all_analysis_metadata: list[AnalysisMetadata] = relationship(
        "AnalysisMetadata", primaryjoin="AnalysisMetadata.observable_uuid == Observable.uuid", lazy="selectin"
    )

    # This gets populated by certain submission-related queries.
    analysis_metadata = None

    context = Column(String)

    # This gets populated by certain submission-related queries.
    disposition_history = None

    # NOTE: You could alter this relationship to directly return a list of EventStatus objects. However,
    # a SQLAlchemy relationship only returns unique/distinct objects. So if an observable appears in multiple events
    # that have the same status, you will only receive a single instance of that status in the relationship.
    #
    # Instead, the relationship is set up to return a list of events, and then an association proxy is used
    # to get a list of the events' statuses.
    events = relationship(
        "Event",
        secondary="join(Event, Submission, Event.uuid == Submission.event_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.submission_uuid == Submission.uuid)."
        "join(analysis_child_observable_mapping, analysis_child_observable_mapping.c.analysis_uuid == submission_analysis_mapping.c.analysis_uuid)",
        primaryjoin="Observable.uuid == analysis_child_observable_mapping.c.observable_uuid",
        viewonly=True,
        lazy="selectin",
    )

    event_statuses: list[EventStatus] = association_proxy("events", "status")

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

    # This gets populated by certain submission-related queries.
    matching_events = None

    relationships = relationship(
        "ObservableRelationship",
        primaryjoin="ObservableRelationship.observable_uuid == Observable.uuid",
        viewonly=True,
        lazy="selectin",
    )

    tags: list[MetadataTag] = relationship("MetadataTag", secondary=observable_tag_mapping, lazy="selectin")

    type = relationship("ObservableType", lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("observable_type.uuid"), nullable=False)

    value = Column(String, nullable=False)

    version = Column(UUID(as_uuid=True), server_default=func.gen_random_uuid(), nullable=False)

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

    def to_dict(self, extra_ignore_keys: Optional[list[str]] = None):
        ignore_keys = [
            "alerts",
            "convert_to_pydantic",
            "history",
            "history_snapshot",
            "to_dict",
        ]

        if extra_ignore_keys:
            ignore_keys += extra_ignore_keys

        return {key: getattr(self, key) for key in self.__class__.__dict__ if key not in ignore_keys}

    @property
    def history_snapshot(self):
        return json.loads(
            ObservableRead(
                **self.to_dict(extra_ignore_keys=["alert_dispositions", "analysis_metadata", "disposition_history"])
            ).json()
        )

    # TODO: Figure out how to sort this within the relationship itself
    @property
    def observable_relationships(self) -> list[ObservableRelationshipRead]:
        """Returns the list of observable relationships for this observable sorted by the
        related observable's type then value"""

        return sorted(self.relationships, key=lambda x: (x.related_observable.type.value, x.related_observable.value))
