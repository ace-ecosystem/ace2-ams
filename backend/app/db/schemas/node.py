from sqlalchemy import func, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.node_directive_mapping import node_directive_mapping
from db.schemas.node_tag_mapping import node_tag_mapping
from db.schemas.node_threat_mapping import node_threat_mapping


# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#joined-table-inheritance
class Node(Base):
    __tablename__ = "node"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    comments = relationship("NodeComment")

    directives = relationship("NodeDirective", secondary=node_directive_mapping)

    node_type = Column(String)

    tags = relationship("NodeTag", secondary=node_tag_mapping)

    threat_actor = relationship("NodeThreatActor")

    threat_actor_uuid = Column(UUID(as_uuid=True), ForeignKey("node_threat_actor.uuid"))

    threats = relationship("NodeThreat", secondary=node_threat_mapping)

    version = Column(UUID(as_uuid=True), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "node", "polymorphic_on": node_type, "with_polymorphic": "*"}

    def serialize_for_node_tree(self):
        raise NotImplementedError("A Node subclass must implement serialize_for_node_tree")
