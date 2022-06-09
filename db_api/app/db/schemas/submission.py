import json

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Optional

from api_models.submission import SubmissionRead, SubmissionTreeRead
from db.database import Base
from db.schemas.analysis import Analysis
from db.schemas.helpers import utcnow
from db.schemas.history import HasHistory, HistoryMixin
from db.schemas.node import Node
from db.schemas.submission_analysis_mapping import submission_analysis_mapping
from db.schemas.tag import Tag


class SubmissionHistory(Base, HistoryMixin):
    __tablename__ = "submission_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("submission.uuid"), index=True, nullable=False)


class Submission(Node, HasHistory):
    __tablename__ = "submission"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert = Column(Boolean, default=False, nullable=False, index=True)

    # Analyses are lazy loaded and are not included by default when fetching a submission from the API.
    analyses: list[Analysis] = relationship("Analysis", secondary=submission_analysis_mapping)

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
    child_detection_points = relationship(
        "NodeDetectionPoint",
        secondary="join(NodeDetectionPoint, Observable, NodeDetectionPoint.node_uuid == Observable.uuid)."
        "join(analysis_child_observable_mapping, analysis_child_observable_mapping.c.observable_uuid == Observable.uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        order_by="asc(NodeDetectionPoint.value)",
        viewonly=True,
        lazy="selectin",
    )

    child_analysis_tags = relationship(
        "Tag",
        secondary="join(Tag, AnalysisMetadata, Tag.uuid == AnalysisMetadata.metadata_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == AnalysisMetadata.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        order_by="asc(Tag.value)",
        viewonly=True,
        lazy="selectin",
    )

    child_threat_actors = relationship(
        "NodeThreatActor",
        secondary="join(NodeThreatActor, node_threat_actor_mapping, NodeThreatActor.uuid == node_threat_actor_mapping.c.threat_actor_uuid)."
        "join(analysis_child_observable_mapping, analysis_child_observable_mapping.c.observable_uuid == node_threat_actor_mapping.c.node_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        order_by="asc(NodeThreatActor.value)",
        viewonly=True,
        lazy="selectin",
    )

    child_threats = relationship(
        "NodeThreat",
        secondary="join(NodeThreat, node_threat_mapping, NodeThreat.uuid == node_threat_mapping.c.threat_uuid)."
        "join(analysis_child_observable_mapping, analysis_child_observable_mapping.c.observable_uuid == node_threat_mapping.c.node_uuid)."
        "join(submission_analysis_mapping, submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid)",
        primaryjoin="Submission.uuid == submission_analysis_mapping.c.submission_uuid",
        order_by="asc(NodeThreat.value)",
        viewonly=True,
        lazy="selectin",
    )

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

    name = Column(String, nullable=False)

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True)

    owner = relationship("User", foreign_keys=[owner_uuid], lazy="selectin")

    # Stores the most recent time the submission changed owners
    ownership_time = Column(DateTime(timezone=True), index=True)

    queue = relationship("Queue", lazy="selectin")

    queue_uuid = Column(UUID(as_uuid=True), ForeignKey("queue.uuid"), nullable=False, index=True)

    root_analysis_uuid = Column(UUID(as_uuid=True), ForeignKey("analysis.uuid"), nullable=False, index=True)

    root_analysis: Analysis = relationship("Analysis", foreign_keys=[root_analysis_uuid], lazy="selectin")

    tool = relationship("SubmissionTool", lazy="selectin")

    tool_uuid = Column(UUID(as_uuid=True), ForeignKey("submission_tool.uuid"), index=True)

    tool_instance = relationship("SubmissionToolInstance", lazy="selectin")

    tool_instance_uuid = Column(UUID(as_uuid=True), ForeignKey("submission_tool_instance.uuid"), index=True)

    type = relationship("SubmissionType", lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("submission_type.uuid"), nullable=False, index=True)

    __mapper_args__ = {"polymorphic_identity": "submission", "polymorphic_load": "inline"}

    __table_args__ = (
        Index(
            "name_trgm",
            name,
            postgresql_ops={"name": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
    )

    def convert_to_pydantic(self) -> SubmissionTreeRead:
        return SubmissionTreeRead(**self.__dict__)

    # TODO: This property eventually needs to include any permanent tags applied to observables.
    @property
    def child_tags(self) -> list[Tag]:
        return self.child_analysis_tags

    @property
    def history_snapshot(self):
        return json.loads(SubmissionRead(**self.__dict__).json())

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
