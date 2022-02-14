from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from typing import Optional

from api.models.event import EventRead
from db.database import Base
from db.schemas.event_prevention_tool_mapping import event_prevention_tool_mapping
from db.schemas.event_remediation_mapping import event_remediation_mapping
from db.schemas.event_vector_mapping import event_vector_mapping
from db.schemas.helpers import utcnow
from db.schemas.history import HistoryMixin
from db.schemas.node import Node


class EventHistory(Base, HistoryMixin):
    __tablename__ = "event_history"

    record_uuid = Column(UUID(as_uuid=True), ForeignKey("event.uuid"), index=True, nullable=False)


class Event(Node):
    __tablename__ = "event"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert_time = Column(DateTime(timezone=True), index=True)

    alerts = relationship("Alert", primaryjoin="Alert.event_uuid == Event.uuid", lazy="selectin")

    alert_uuids = association_proxy("alerts", "uuid")

    # There isn't currently a way to automatically calculate this time
    contain_time = Column(DateTime(timezone=True), index=True)

    creation_time = Column(DateTime(timezone=True), server_default=utcnow(), index=True)

    disposition_time = Column(DateTime(timezone=True), index=True)

    event_time = Column(DateTime(timezone=True), index=True)

    history = relationship(
        "EventHistory",
        primaryjoin="EventHistory.record_uuid == Event.uuid",
        lazy="selectin",
        order_by="EventHistory.action_time",
    )

    name = Column(String, nullable=False)

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), nullable=True)

    owner = relationship("User", foreign_keys=[owner_uuid], lazy="selectin")

    ownership_time = Column(DateTime(timezone=True), index=True)

    prevention_tools = relationship("EventPreventionTool", secondary=event_prevention_tool_mapping, lazy="selectin")

    queue = relationship("EventQueue", lazy="selectin")

    queue_uuid = Column(UUID(as_uuid=True), ForeignKey("event_queue.uuid"), nullable=False, index=True)

    # There isn't currently a way to automatically calculate this time
    remediation_time = Column(DateTime(timezone=True), index=True)

    remediations = relationship("EventRemediation", secondary=event_remediation_mapping, lazy="selectin")

    risk_level = relationship("EventRiskLevel", lazy="selectin")

    risk_level_uuid = Column(UUID(as_uuid=True), ForeignKey("event_risk_level.uuid"))

    source = relationship("EventSource", lazy="selectin")

    source_uuid = Column(UUID(as_uuid=True), ForeignKey("event_source.uuid"))

    status = relationship("EventStatus", lazy="selectin")

    status_uuid = Column(UUID(as_uuid=True), ForeignKey("event_status.uuid"), nullable=False)

    type = relationship("EventType", lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("event_type.uuid"))

    vectors = relationship("EventVector", secondary=event_vector_mapping, lazy="selectin")

    __mapper_args__ = {"polymorphic_identity": "event", "polymorphic_load": "inline"}

    def serialize_for_node_tree(self) -> EventRead:
        return EventRead(**self.__dict__)

    @property
    def auto_alert_time(self) -> Optional[datetime]:
        """Returns the earliest time an alert in the event was created"""
        if self.alerts:
            return sorted(self.alerts, key=lambda x: x.insert_time)[0].insert_time
        return None

    @property
    def auto_disposition_time(self) -> Optional[datetime]:
        """Returns the earliest time an alert in the event was dispositioned"""
        if self.alerts:
            return sorted(
                self.alerts, key=lambda x: (x.disposition_time_earliest is None, x.disposition_time_earliest)
            )[0].disposition_time_earliest
        return None

    @property
    def auto_event_time(self) -> Optional[datetime]:
        """Returns the earliest event time from the alerts in the event"""
        if self.alerts:
            return sorted(self.alerts, key=lambda x: x.event_time)[0].event_time
        return None

    @property
    def auto_ownership_time(self) -> Optional[datetime]:
        """Returns the earliest time an analyst took ownership of an alert in the event"""
        if self.alerts:
            return sorted(self.alerts, key=lambda x: (x.ownership_time_earliest is None, x.ownership_time_earliest))[
                0
            ].ownership_time_earliest
        return None
