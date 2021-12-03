from sqlalchemy import Column, ForeignKey, func, Index
from sqlalchemy.dialects.postgresql import UUID

from db.database import Base


class NodeTree(Base):
    __tablename__ = "node_tree"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    root_node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), nullable=False, index=True)

    node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), nullable=False)

    parent_node_uuid = Column(UUID(as_uuid=True), ForeignKey("node.uuid"), nullable=True)

    # These two partial indices combine to enforce the uniqueness of root_node_uuid + node_uuid + parent_node_uuid
    # even when the parent_node_uuid is NULL. This is so that you cannot create the same NodeTree entry twice.
    __table_args__ = (
        Index(
            "uix_root_node_parent",
            "root_node_uuid",
            "node_uuid",
            "parent_node_uuid",
            unique=True,
            postgresql_where=parent_node_uuid.isnot(None),
        ),
        Index("uix_root_node", "root_node_uuid", "node_uuid", unique=True, postgresql_where=parent_node_uuid.is_(None)),
    )
