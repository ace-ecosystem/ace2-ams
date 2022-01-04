from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from api.models.event import EventRead
from db.schemas.event_prevention_tool_mapping import event_prevention_tool_mapping
from db.schemas.event_remediation_mapping import event_remediation_mapping
from db.schemas.event_vector_mapping import event_vector_mapping
from db.schemas.helpers import utcnow
from db.schemas.node import Node


class Event(Node):
    __tablename__ = "event"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    alert_time = Column(DateTime(timezone=True))

    alerts = relationship("Alert", primaryjoin="Alert.event_uuid == Event.uuid")

    alert_uuids = association_proxy("alerts", "uuid")

    contain_time = Column(DateTime(timezone=True))

    creation_time = Column(DateTime(timezone=True), server_default=utcnow())

    disposition_time = Column(DateTime(timezone=True))

    event_time = Column(DateTime(timezone=True))

    name = Column(String, nullable=False)

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), nullable=True)

    owner = relationship("User", foreign_keys=[owner_uuid])

    ownership_time = Column(DateTime(timezone=True))

    prevention_tools = relationship("EventPreventionTool", secondary=event_prevention_tool_mapping)

    remediation_time = Column(DateTime(timezone=True))

    remediations = relationship("EventRemediation", secondary=event_remediation_mapping)

    risk_level = relationship("EventRiskLevel")

    risk_level_uuid = Column(UUID(as_uuid=True), ForeignKey("event_risk_level.uuid"))

    source = relationship("EventSource")

    source_uuid = Column(UUID(as_uuid=True), ForeignKey("event_source.uuid"))

    status = relationship("EventStatus")

    status_uuid = Column(UUID(as_uuid=True), ForeignKey("event_status.uuid"))

    type = relationship("EventType")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("event_type.uuid"))

    vectors = relationship("EventVector", secondary=event_vector_mapping)

    __mapper_args__ = {"polymorphic_identity": "event", "polymorphic_load": "inline"}

    def serialize_for_node_tree(self) -> EventRead:
        return EventRead(**self.__dict__)
