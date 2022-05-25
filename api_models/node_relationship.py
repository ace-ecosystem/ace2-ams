from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str
from api_models.node import NodeRead
from api_models.node_relationship_type import NodeRelationshipTypeRead


class NodeRelationshipBase(BaseModel):
    """Represents a node relationship that can be applied to a node (typically an observable)."""

    node_uuid: UUID4 = Field(description="The UUID of the node")


class NodeRelationshipCreate(NodeRelationshipBase):
    history_username: Optional[type_str] = Field(
        description="If given, a history record will be created and associated with the user"
    )

    related_node_uuid: UUID4 = Field(description="The UUID of the related node")

    type: type_str = Field(description="The type of the node relationship")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the node relationship")


class NodeRelationshipRead(NodeRelationshipBase):
    uuid: UUID4 = Field(description="The UUID of the node relationship")

    related_node: NodeRead = Field(description="The related node")

    type: NodeRelationshipTypeRead = Field(description="The type of the node relationship")

    class Config:
        orm_mode = True
