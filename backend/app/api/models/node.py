from pydantic import BaseModel, Field, UUID4
from typing import Dict, List, Optional
from uuid import uuid4

from api.models import type_str


class NodeBase(BaseModel):
    """Represents an individual node."""

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

    version: UUID4 = Field(
        default_factory=uuid4,
        description="""A version string that automatically changes every time the node is modified. The version
            must match when updating.""",
    )


class NodeCreate(NodeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node")


class NodeRead(NodeBase):

    node_type: type_str = Field(description="The type of the Node")

    uuid: UUID4 = Field(description="The UUID of the node")

    class Config:
        orm_mode = True


class NodeUpdate(NodeBase):
    # The version is optional when updating a Node since certain actions in the GUI do not need to care
    # about the version. However, if the version is given, the update will be rejected if it does not match.
    version: Optional[UUID4] = Field(
        description="""A version string that automatically changes every time the node is modified. If supplied,
        the version must match when updating.""",
    )


class NodeTreeBase(BaseModel):
    """Represents a leaf in a Node tree."""

    node_uuid: UUID4 = Field(description="The UUID of the Node represented by the leaf")

    root_node_uuid: UUID4 = Field(
        description="""The Node UUID that contains the tree.
            For example, an alert UUID that contains a tree of analyses and observables."""
    )

    parent_tree_uuid: Optional[UUID4] = Field(description="The UUID of the parent leaf")

    class Config:
        orm_mode = True


class NodeTreeMetadataDisplay(BaseModel):
    type: Optional[type_str] = Field(description="An optional type override to use when displaying the Node in the GUI")

    value: Optional[type_str] = Field(
        description="An optional value override to use when displaying the Node in the GUI"
    )


class NodeTreeMetadata(BaseModel):
    display: Optional[NodeTreeMetadataDisplay] = Field(
        description="Optional attributes to include that will override how the Node is displayed in the GUI"
    )


class NodeTreeCreateWithNode(BaseModel):
    node_metadata: Optional[NodeTreeMetadata] = Field(description="Optional metadata included with the Node")

    root_node_uuid: UUID4 = Field(
        description="""The node UUID that contains the tree.
            For example, an alert UUID that contains a tree of analyses and observables."""
    )

    parent_tree_uuid: Optional[UUID4] = Field(description="The UUID of the leaf in the tree that should be the parent")


class NodeTreeItemRead(NodeRead):
    children: List[Dict] = Field(default_factory=list, description="A list of this Node's child Nodes")

    first_appearance: bool = Field("Whether or not this is the first time the Node appears in the tree")

    node_metadata: Optional[NodeTreeMetadata] = Field(description="Optional metadata included with the Node")

    parent_tree_uuid: Optional[UUID4] = Field(
        description="The node's parent leaf UUID if the node is inside a NodeTree"
    )

    tree_uuid: UUID4 = Field(description="The UUID of the leaf if this Node is inside a NodeTree")


class NodeVersion(BaseModel):
    version: UUID4 = Field(description="The current version of the Node")

    class Config:
        orm_mode = True
