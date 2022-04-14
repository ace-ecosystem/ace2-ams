from sqlalchemy import func, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base
from db.schemas.node_directive_mapping import node_directive_mapping
from db.schemas.node_tag_mapping import node_tag_mapping
from db.schemas.node_threat_actor_mapping import node_threat_actor_mapping
from db.schemas.node_threat_mapping import node_threat_mapping


# https://docs.sqlalchemy.org/en/14/orm/inheritance.html#joined-table-inheritance
class Node(Base):
    __tablename__ = "node"

    uuid = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())

    # The child_tags field uses a composite join relationship to get a list of the tags that
    # are applied to any Nodes that exist in this Node's tree structure. For example, this is
    # used on the Manage Alerts page so that we can display ALL of the tags for an alert and
    # its child Nodes. Below is an example of a raw SQL query that gets a list of the tags
    # on child Nodes:
    #
    # SELECT * from node_tag
    # JOIN node_tag_mapping ON node_tag_mapping.tag_uuid = node_tag.uuid
    # JOIN node_tree ON node_tree.node_uuid = node_tag_mapping.node_uuid
    # WHERE node_tree.root_node_uuid = '02f8299b-2a24-400f-9751-7dd9164daf6a'
    # AND node_tree.node_uuid != '02f8299b-2a24-400f-9751-7dd9164daf6a'
    #
    # While there is nothing complicated about this SQL query, SQLAlchemy does not have a
    # straightforward way to handle these types of relationships with intermediate tables.
    # To solve this, you have to use the composite join relationship, which is described here:
    # https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#composite-secondary-joins
    #
    # The overall goal is that you use the "secondary" parameter in the relationship to construct
    # the intermediate table that you need. You then use the "primaryjoin" and, if needed, the
    # "secondaryjoin" parameters to tell SQLAlchemy how to join the child object against the
    # parent object (where in this case Node is the parent, and NodeTag is the child).
    #
    # Finally, "viewonly" is used on the relationship to prevent attempts to add tags to this list.

    child_tags = relationship(
        "NodeTag",
        secondary="join(NodeTag, node_tag_mapping, NodeTag.uuid == node_tag_mapping.c.tag_uuid)."
        "join(NodeTree, NodeTree.node_uuid == node_tag_mapping.c.node_uuid)",
        primaryjoin="and_(Node.uuid == NodeTree.root_node_uuid, Node.uuid != NodeTree.node_uuid)",
        viewonly=True,
        lazy="selectin",
    )

    child_threat_actors = relationship(
        "NodeThreatActor",
        secondary="join(NodeThreatActor, node_threat_actor_mapping, NodeThreatActor.uuid == node_threat_actor_mapping.c.threat_actor_uuid)."
        "join(NodeTree, NodeTree.node_uuid == node_threat_actor_mapping.c.node_uuid)",
        primaryjoin="and_(Node.uuid == NodeTree.root_node_uuid, Node.uuid != NodeTree.node_uuid)",
        viewonly=True,
        lazy="selectin",
    )

    child_threats = relationship(
        "NodeThreat",
        secondary="join(NodeThreat, node_threat_mapping, NodeThreat.uuid == node_threat_mapping.c.threat_uuid)."
        "join(NodeTree, NodeTree.node_uuid == node_threat_mapping.c.node_uuid)",
        primaryjoin="and_(Node.uuid == NodeTree.root_node_uuid, Node.uuid != NodeTree.node_uuid)",
        viewonly=True,
        lazy="selectin",
    )

    comments = relationship("NodeComment", lazy="selectin")

    detection_points = relationship("NodeDetectionPoint", lazy="selectin")

    directives = relationship("NodeDirective", secondary=node_directive_mapping, lazy="selectin")

    node_type = Column(String)

    relationships = relationship(
        "NodeRelationship",
        primaryjoin="NodeRelationship.node_uuid == Node.uuid",
        viewonly=True,
        lazy="selectin",
    )

    tags = relationship("NodeTag", secondary=node_tag_mapping, lazy="selectin")

    threat_actors = relationship("NodeThreatActor", secondary=node_threat_actor_mapping, lazy="selectin")

    threats = relationship("NodeThreat", secondary=node_threat_mapping, lazy="selectin")

    version = Column(UUID(as_uuid=True), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "node", "polymorphic_on": node_type, "with_polymorphic": "*"}

    def serialize_for_node_tree(self):
        raise NotImplementedError("A Node subclass must implement serialize_for_node_tree")
