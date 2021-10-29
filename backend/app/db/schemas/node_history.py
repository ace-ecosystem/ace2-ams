from sqlalchemy import func, Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.helpers import utcnow


class NodeHistory(Base):
    __tablename__ = "node_history"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    action = relationship("NodeHistoryAction")

    action_uuid = Column(UUID(as_uuid=True), ForeignKey("node_history_action.uuid"))

    action_user_uuid = Column(UUID(as_uuid=True), ForeignKey("user.uuid"))

    action_user = relationship("User", foreign_keys=[action_user_uuid])

    after = Column(JSONB)

    before = Column(JSONB)

    node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"))

    node = relationship("Node", foreign_keys=[node_uuid])

    timestamp = Column(DateTime, server_default=utcnow())
