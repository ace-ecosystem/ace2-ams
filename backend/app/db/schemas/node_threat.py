from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.node_threat_node_threat_type_mapping import (
    node_threat_node_threat_type_mapping,
)
from db.schemas.node_threat_queue_mapping import node_threat_queue_mapping


class NodeThreat(Base):
    __tablename__ = "node_threat"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    description = Column(String)

    queues = relationship("Queue", secondary=node_threat_queue_mapping, lazy="selectin")

    types = relationship(
        "NodeThreatType",
        secondary=node_threat_node_threat_type_mapping,
        passive_deletes=True,
    )

    value = Column(String, nullable=False, unique=True, index=True)
