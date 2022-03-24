from sqlalchemy import Column, ForeignKey, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class NodeRelationship(Base):
    __tablename__ = "node_relationship"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), index=True)

    # The node relationship is not loaded automatically
    node = relationship("Node", foreign_keys=[node_uuid])

    related_node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"))

    related_node = relationship("Node", foreign_keys=[related_node_uuid], lazy="selectin")

    type_uuid = Column(UUID(as_uuid=True), ForeignKey("node_relationship_type.uuid"))

    type = relationship("NodeRelationshipType", foreign_keys=[type_uuid], lazy="selectin")

    __table_args__ = (UniqueConstraint("node_uuid", "related_node_uuid", "type_uuid", name="node_related_type_uc"),)
