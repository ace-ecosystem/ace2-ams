from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.node_threat_actor_queue_mapping import node_threat_actor_queue_mapping


class NodeThreatActor(Base):
    __tablename__ = "node_threat_actor"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    description = Column(String)

    queues = relationship("Queue", secondary=node_threat_actor_queue_mapping, lazy="selectin")

    value = Column(String, nullable=False, unique=True, index=True)
