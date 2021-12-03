from pydantic import BaseModel, Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api.models import type_str
from api.models.node_comment import NodeCommentRead
from api.models.node_directive import NodeDirectiveRead
from api.models.node_tag import NodeTagRead
from api.models.node_threat import NodeThreatRead
from api.models.node_threat_actor import NodeThreatActorRead


class NodeBase(BaseModel):
    """Represents an individual node."""

    directives: List[type_str] = Field(default_factory=list, description="A list of directives to add to the node")

    # TODO: Add a node_links_mapping table
    # links: Optional[List[UUID]] = Field(
    #     default_factory=list,
    #     description="The list of node UUIDs linked to this node. Nodes that are linked receive the same tags."
    # )

    # TODO: Add a node_relationships table and node_relationship_mapping table
    # relationships: Optional[Dict[type_str, List[UUID]]] = Field(
    #     default_factory=list,
    #     description="""A mapping of relationships between this node and other nodes. The key is the name of the
    #         relationship. The value for each key is a list of one or more node UUIDs related in this way."""
    # )

    tags: List[type_str] = Field(default_factory=list, description="A list of tags to add to the node")

    threat_actor: Optional[type_str] = Field(description="The threat actor to add to the node")

    threats: List[type_str] = Field(default_factory=list, description="A list of threats to add to the node")

    version: UUID4 = Field(
        default_factory=uuid4,
        description="""A version string that automatically changes every time the node is modified. The version
            must match when updating.""",
    )


class NodeCreate(NodeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node")


class NodeRead(NodeBase):
    comments: List[NodeCommentRead] = Field(description="A list of comments added to the node")

    directives: List[NodeDirectiveRead] = Field(description="A list of directives added to the node")

    parent_uuid: Optional[UUID4] = Field(description="The node's parent UUID if the node is inside a node tree")

    tags: List[NodeTagRead] = Field(description="A list of tags added to the node")

    threat_actor: Optional[NodeThreatActorRead] = Field(description="The threat actor added to the node")

    threats: List[NodeThreatRead] = Field(description="A list of threats added to the node")

    uuid: UUID4 = Field(description="The UUID of the node")

    class Config:
        orm_mode = True


class NodeUpdate(NodeBase):
    directives: Optional[List[type_str]] = Field(description="A list of directives applied to the node")

    tags: Optional[List[type_str]] = Field(description="A list of tags to add to the node")

    threats: Optional[List[type_str]] = Field(description="A list of threats to add to the node")

    # In order to update any Node, you must pass in the version that you want to update. If the version does not
    # match, then the update will fail.
    version: UUID4 = Field(
        description="""The version of the Node being updated. This must match its current version to succeed."""
    )


class NodeTreeBase(BaseModel):
    """Represents a leaf in a Node tree."""

    node_uuid: UUID4 = Field(description="The node UUID of the leaf")

    root_node_uuid: UUID4 = Field(
        description="""The node UUID that contains the tree.
            For example, an alert UUID that contains a tree of analyses and observables."""
    )

    parent_node_uuid: Optional[UUID4] = Field(description="The node UUID of the leaf node")

    class Config:
        orm_mode = True


class NodeTreeCreateWithNode(BaseModel):
    root_node_uuid: UUID4 = Field(
        description="""The node UUID that contains the tree.
            For example, an alert UUID that contains a tree of analyses and observables."""
    )

    parent_node_uuid: Optional[UUID4] = Field(description="The node UUID of the leaf node")


class NodeTreeRead(BaseModel):
    root_node: NodeRead = Field(description="The root node of the tree. For example, this will often be an Alert.")

    leaves: List[NodeTreeBase] = Field(description="A list of the Node leaves that make up the tree")

    class Config:
        orm_mode = True


class NodeTreeUpdate(NodeTreeBase):
    root_node_uuid: Optional[UUID4] = Field(
        description="""The node UUID that contains the tree.
            For example, an alert UUID that contains a tree of analyses and observables."""
    )

    node_uuid: Optional[UUID4] = Field(description="The node UUID of the leaf")
