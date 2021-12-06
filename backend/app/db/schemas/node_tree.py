from sqlalchemy import Column, ForeignKey, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class NodeTree(Base):
    __tablename__ = "node_tree"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    root_node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), nullable=False, index=True)

    root_node = relationship("Node", foreign_keys=[root_node_uuid])

    node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), nullable=False)

    node = relationship("Node", foreign_keys=[node_uuid])

    parent_tree_uuid = Column(UUID(as_uuid=True), ForeignKey("node_tree.uuid"), nullable=True)

    parent_tree = relationship("NodeTree", foreign_keys=[parent_tree_uuid])

    # These two partial indices combine to enforce the uniqueness of root_node_uuid + node_uuid + parent_tree_uuid
    # even when the parent_tree_uuid is NULL. This is so that you cannot create the same NodeTree entry twice.
    __table_args__ = (
        Index(
            "uix_root_node_parent",
            "root_node_uuid",
            "node_uuid",
            "parent_tree_uuid",
            unique=True,
            postgresql_where=parent_tree_uuid.isnot(None),
        ),
        Index("uix_root_node", "root_node_uuid", "node_uuid", unique=True, postgresql_where=parent_tree_uuid.is_(None)),
    )
