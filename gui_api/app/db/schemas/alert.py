import json

from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from typing import Optional

from api_models.alert import AlertRead, AlertTreeRead
from db.database import Base
from db.schemas.helpers import utcnow
from db.schemas.history import HasHistory, HistoryMixin
from db.schemas.node import Node


class AlertHistory(Base, HistoryMixin):
    __tablename__ = "alert_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("alert.uuid"), index=True, nullable=False)


class Alert(Node, HasHistory):
    __tablename__ = "alert"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    description = Column(String)

    disposition = relationship("AlertDisposition", lazy="selectin")

    disposition_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_disposition.uuid"), index=True)

    # Stores the most recent time the alert was dispositioned.
    # Needed for the "sort by disposition_time" feature.
    disposition_time = Column(DateTime(timezone=True), index=True)

    # Stores the user UUID of who most recently dispositioned the alert.
    # Needed for the "sort by disposition_user" feature.
    disposition_user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True)

    disposition_user = relationship("User", foreign_keys=[disposition_user_uuid], lazy="selectin")

    event_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False, index=True)

    event_uuid = Column(UUID(as_uuid=True), ForeignKey("event.uuid"), index=True)

    event = relationship("Event", foreign_keys=[event_uuid])

    # History is lazy loaded and is not included by default when fetching an alert from the API.
    history = relationship(
        "AlertHistory",
        primaryjoin="AlertHistory.record_uuid == Alert.uuid",
        order_by="AlertHistory.action_time",
    )

    insert_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False, index=True)

    instructions = Column(String)

    name = Column(String, nullable=False)

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True)

    owner = relationship("User", foreign_keys=[owner_uuid], lazy="selectin")

    queue = relationship("Queue", lazy="selectin")

    queue_uuid = Column(UUID(as_uuid=True), ForeignKey("queue.uuid"), nullable=False, index=True)

    tool = relationship("AlertTool", lazy="selectin")

    tool_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_tool.uuid"), index=True)

    tool_instance = relationship("AlertToolInstance", lazy="selectin")

    tool_instance_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_tool_instance.uuid"), index=True)

    type = relationship("AlertType", lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_type.uuid"), nullable=False, index=True)

    __mapper_args__ = {"polymorphic_identity": "alert", "polymorphic_load": "inline"}

    __table_args__ = (
        Index(
            "name_trgm",
            name,
            postgresql_ops={"name": "gin_trgm_ops"},
            postgresql_using="gin",
        ),
    )

    def serialize_for_node_tree(self) -> AlertTreeRead:
        return AlertTreeRead(**self.__dict__)

    @property
    def history_snapshot(self):
        return json.loads(AlertRead(**self.__dict__).json())

    @property
    def disposition_time_earliest(self) -> Optional[datetime]:
        """Returns the earliest time the alert was dispositioned"""
        history: Optional[AlertHistory] = next((x for x in self.history if x.field == "disposition"), None)
        if history:
            return history.action_time
        return None

    @property
    def ownership_time_earliest(self) -> Optional[datetime]:
        """Returns the earliest time an analyst took ownership of the alert"""
        history: Optional[AlertHistory] = next((x for x in self.history if x.field == "owner"), None)
        if history:
            return history.action_time
        return None
