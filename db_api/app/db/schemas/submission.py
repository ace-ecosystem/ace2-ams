import json

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from typing import Optional

from api_models.submission import SubmissionRead, SubmissionTreeRead
from db.database import Base
from db.schemas.analysis import Analysis
from db.schemas.helpers import utcnow
from db.schemas.history import HasHistory, HistoryMixin
from db.schemas.metadata_detection_point import MetadataDetectionPoint
from db.schemas.metadata_tag import MetadataTag
from db.schemas.observable import Observable
from db.schemas.submission_analysis_mapping import submission_analysis_mapping
from db.schemas.submission_tag_mapping import submission_tag_mapping


class SubmissionHistory(Base, HistoryMixin):
    __tablename__ = "submission_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("submission.uuid"), index=True, nullable=False)


class Submission(Base, HasHistory):
    __tablename__ = "submission"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    alert = Column(Boolean, default=False, nullable=False, index=True)

    # Analyses are lazy loaded and are not included by default when fetching a submission from the API.
    analyses: list[Analysis] = relationship("Analysis", secondary=submission_analysis_mapping)

    analysis_uuids: list[UUID] = association_proxy("analyses", "uuid")

    # The child_* fields use a composite join relationship to get a list of the objects that
    # are applied to any observables that exist in this submission's tree structure. For example, this is
    # used on the Manage Alerts page so that we can display ALL of the tags for a submission and
    # its children.
    #
    # While there is nothing too complicated about this SQL query, SQLAlchemy does not have a
    # straightforward way to handle these types of relationships with intermediate tables.
    # To solve this, you have to use the composite join relationship, which is described here:
    # https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#composite-secondary-joins
    #
    # The overall goal is that you use the "secondary" parameter in the relationship to construct
    # the intermediate table that you need. You then use the "primaryjoin" and, if needed, the
    # "secondaryjoin" parameters to tell SQLAlchemy how to join the child object against the
    # parent object (where in this case Submission is the parent, and the child object is the child).
    #
    # Finally, "viewonly" is used on the relationship to prevent attempts to add tags to this list.

    child_analysis_tags: list[MetadataTag] = relationship(
        "MetadataTag",
        secondary="join(AnalysisMetadata, MetadataTag, MetadataTag.uuid == AnalysisMetadata.metadata_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == AnalysisMetadata.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        # NOTE: The secondaryjoin parameter is required specifically when using the
        # crud.submission.read_all() function to filter submissions by their tags.
        # Without it, the query that SQLAlchemy creates results in the returned submissions
        # having every tag from every submission in their child_analysis_tags list.
        secondaryjoin="Metadata.uuid == AnalysisMetadata.metadata_uuid",
        order_by="asc(MetadataTag.value)",
        viewonly=True,
        lazy="selectin",
    )

    child_detection_points: list[MetadataDetectionPoint] = relationship(
        "MetadataDetectionPoint",
        secondary="join(AnalysisMetadata, MetadataDetectionPoint, MetadataDetectionPoint.uuid == AnalysisMetadata.metadata_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == AnalysisMetadata.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        secondaryjoin="Metadata.uuid == AnalysisMetadata.metadata_uuid",
        order_by="asc(MetadataDetectionPoint.value)",
        viewonly=True,
        lazy="selectin",
    )

    # The relationship is lazy loaded since not everything requires it.
    child_observables: list[Observable] = relationship(
        "Observable",
        secondary="join(Observable, analysis_child_observable_mapping, Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        viewonly=True,
    )

    child_tags: list[MetadataTag] = relationship(
        "MetadataTag",
        secondary="join(MetadataTag, observable_tag_mapping, MetadataTag.uuid == observable_tag_mapping.c.tag_uuid)."
        "join(analysis_child_observable_mapping, analysis_child_observable_mapping.c.observable_uuid == observable_tag_mapping.c.observable_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        secondaryjoin="MetadataTag.uuid == observable_tag_mapping.c.tag_uuid",
        foreign_keys="[Submission.uuid, MetadataTag.uuid]",
        order_by="asc(MetadataTag.value)",
        viewonly=True,
        lazy="selectin",
    )

    comments = relationship("SubmissionComment", lazy="selectin", viewonly=True)

    description = Column(String)

    disposition = relationship("AlertDisposition", lazy="selectin")

    disposition_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_disposition.uuid"), index=True)

    # Stores the most recent time the submission was dispositioned.
    # Needed for the "sort by disposition_time" feature.
    disposition_time = Column(DateTime(timezone=True), index=True)

    # Stores the user UUID of who most recently dispositioned the submission.
    # Needed for the "sort by disposition_user" feature.
    disposition_user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True)

    disposition_user = relationship("User", foreign_keys=[disposition_user_uuid], lazy="selectin")

    event_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False, index=True)

    event_uuid = Column(UUID(as_uuid=True), ForeignKey("event.uuid"), index=True)

    event = relationship("Event", foreign_keys=[event_uuid])

    # History is lazy loaded and is not included by default when fetching a submission from the API.
    history = relationship(
        "SubmissionHistory",
        primaryjoin="SubmissionHistory.record_uuid == Submission.uuid",
        order_by="SubmissionHistory.action_time",
    )

    insert_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False, index=True)

    instructions = Column(String)

    # This gets populated by certain submission-related queries.
    matching_events = None

    name = Column(String, nullable=False)

    # This gets populated by certain submission-related queries.
    number_of_observables = 0

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True)

    owner = relationship("User", foreign_keys=[owner_uuid], lazy="selectin")

    # Stores the most recent time the submission changed owners
    ownership_time = Column(DateTime(timezone=True), index=True)

    queue = relationship("Queue", lazy="selectin")

    queue_uuid = Column(UUID(as_uuid=True), ForeignKey("queue.uuid"), nullable=False, index=True)

    root_analysis_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"), nullable=False, index=True)

    root_analysis: Analysis = relationship("Analysis", foreign_keys=[root_analysis_uuid], lazy="selectin")

    tags: list[MetadataTag] = relationship("MetadataTag", secondary=submission_tag_mapping, lazy="selectin")

    tool = relationship("SubmissionTool", lazy="selectin")

    tool_uuid = Column(UUID(as_uuid=True), ForeignKey("submission_tool.uuid"), index=True)

    tool_instance = relationship("SubmissionToolInstance", lazy="selectin")

    tool_instance_uuid = Column(UUID(as_uuid=True), ForeignKey("submission_tool_instance.uuid"), index=True)

    type = relationship("SubmissionType", lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("submission_type.uuid"), nullable=False, index=True)

    version = Column(UUID(as_uuid=True), server_default=func.gen_random_uuid(), nullable=False)

    __table_args__ = (
        Index(
            "name_trgm",
            name,
            postgresql_ops={"name": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
    )

    def convert_to_pydantic(self, root_analysis) -> SubmissionTreeRead:
        return SubmissionTreeRead(root_analysis=root_analysis, **self.to_dict())

    def to_dict(self, extra_ignore_keys: Optional[list[str]] = None):
        ignore_keys = [
            "analyses",
            "analysis_uuids",
            "child_observables",
            "event",
            "history",
            "history_snapshot",
            "root_analysis",
            "to_dict",
        ]

        if extra_ignore_keys:
            ignore_keys += extra_ignore_keys

        return {key: getattr(self, key) for key in self.__class__.__dict__ if key not in ignore_keys}

    @property
    def history_snapshot(self):
        return json.loads(
            SubmissionRead(
                **self.to_dict(
                    extra_ignore_keys=[
                        "child_analysis_tags",
                        "child_detection_points",
                        "child_tags",
                    ]
                )
            ).json()
        )

    @property
    def disposition_time_earliest(self) -> Optional[datetime]:
        """Returns the earliest time the submission was dispositioned"""
        history: Optional[SubmissionHistory] = next((x for x in self.history if x.field == "disposition"), None)
        if history:
            return history.action_time
        return None

    @property
    def ownership_time_earliest(self) -> Optional[datetime]:
        """Returns the earliest time an analyst took ownership of the submission"""
        history: Optional[SubmissionHistory] = next((x for x in self.history if x.field == "owner"), None)
        if history:
            return history.action_time
        return None


from api_models.analysis import RootAnalysisSubmissionTreeRead

RootAnalysisSubmissionTreeRead.update_forward_refs()
