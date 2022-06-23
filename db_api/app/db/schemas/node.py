from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.node_threat_actor_mapping import node_threat_actor_mapping
from db.schemas.node_threat_mapping import node_threat_mapping


# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#joined-table-inheritance
class Node(Base):
    __tablename__ = "node"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    comments = relationship("NodeComment", lazy="selectin")

    object_type = Column(String)

    threat_actors = relationship("NodeThreatActor", secondary=node_threat_actor_mapping, lazy="selectin")

    threats = relationship("NodeThreat", secondary=node_threat_mapping, lazy="selectin")

    version = Column(UUID(as_uuid=True), server_default=func.gen_random_uuid(), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "node", "polymorphic_on": object_type, "with_polymorphic": "*"}

    def convert_to_pydantic(self):  # pragma: no cover
        raise NotImplementedError("A Node subclass must implement convert_to_pydantic")
