from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str


class NodeBase(BaseModel):
    """Represents an individual node."""

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


class NodeVersion(BaseModel):
    version: UUID4 = Field(description="The current version of the Node")

    class Config:
        orm_mode = True
