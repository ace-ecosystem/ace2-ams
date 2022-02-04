from sqlalchemy import Column, DateTime, ForeignKey, func, Index, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from api.models.alert import AlertTreeRead
from db.database import Base
from db.schemas.node import Node
from db.schemas.helpers import utcnow


class AlertHistory(Base):
    __tablename__ = "alert_history"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    action = Column(String, nullable=False)

    action_by = Column(String, nullable=False)

    action_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False)

    record_uuid = Column(UUID(as_uuid=True), index=True, nullable=False)

    field = Column(String)

    diff = Column(JSONB)


class Alert(Node):
    __tablename__ = "alert"

    uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), primary_key=True)

    description = Column(String)

    disposition = relationship("AlertDisposition", lazy="selectin")

    disposition_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_disposition.uuid"), index=True)

    disposition_time = Column(DateTime(timezone=True), index=True)

    disposition_user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True)

    disposition_user = relationship("User", foreign_keys=[disposition_user_uuid], lazy="selectin")

    event_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False, index=True)

    event_uuid = Column(UUID(as_uuid=True), ForeignKey("event.uuid"), index=True)

    event = relationship("Event", foreign_keys=[event_uuid])

    insert_time = Column(DateTime(timezone=True), server_default=utcnow(), nullable=False, index=True)

    instructions = Column(String)

    name = Column(String, nullable=False)

    owner_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"), index=True)

    owner = relationship("User", foreign_keys=[owner_uuid], lazy="selectin")

    queue = relationship("AlertQueue", lazy="selectin")

    queue_uuid = Column(UUID(as_uuid=True), ForeignKey("alert_queue.uuid"), nullable=False, index=True)

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
