from datetime import datetime
from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str


class NodeDetectionPointBase(BaseModel):
    """Represents a detection point that can be added to a node."""

    node_uuid: UUID4 = Field(description="The UUID of the node associated with this detection point")

    value: type_str = Field(description="The value of the detection point")


class NodeDetectionPointCreate(NodeDetectionPointBase):
    history_username: Optional[type_str] = Field(
        description="If given, a history record will be created and associated with the user"
    )

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the detection point")


class NodeDetectionPointRead(NodeDetectionPointBase):
    insert_time: datetime = Field(description="The time the detection point was made")

    uuid: UUID4 = Field(description="The UUID of the detection point")

    class Config:
        orm_mode = True


class NodeDetectionPointUpdate(BaseModel):
    # The only thing that makes sense to be able to update is the actual value of the detection point.
    # Otherwise, you would delete the detection point and create a new one.
    value: type_str = Field(description="The value of the detection point")
