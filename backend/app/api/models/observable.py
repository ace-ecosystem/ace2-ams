from datetime import datetime
from pydantic import Field, StrictBool, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators
from api.models.node import NodeBase, NodeCreate, NodeRead, NodeTreeCreateWithNode, NodeUpdate
from api.models.observable_type import ObservableTypeRead


class ObservableBase(NodeBase):
    """Represents a unique observable (based on the type+value)."""

    context: Optional[type_str] = Field(
        description="""Optional context surrounding the observation. This is used to communicate additional information
            to the analysts, such as where the observation was made. For example, 'Source IP address of the sender of
            the email.' or 'From address in the email.'"""
    )

    expires_on: Optional[datetime] = Field(
        description="The time the observable will expire and no longer be included in observable detection exports"
    )

    for_detection: StrictBool = Field(
        default=False,
        description="Whether or not this observable should be included in the observable detection exports",
    )

    redirection_uuid: Optional[UUID4] = Field(
        description="The UUID of another observable to which this one should point"
    )

    time: datetime = Field(default_factory=datetime.utcnow, description="The time this observable was observed")

    type: type_str = Field(description="The type of the observable")

    value: type_str = Field(description="The value of the observable")


class ObservableCreateBase(NodeCreate, ObservableBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable")


class ObservableCreateWithAlert(ObservableCreateBase):
    pass


class ObservableCreate(ObservableCreateBase):
    node_tree: NodeTreeCreateWithNode = Field(description="This defines where in a Node Tree this observable fits")


class ObservableRead(NodeRead, ObservableBase):
    type: ObservableTypeRead = Field(description="The type of the observable")

    uuid: UUID4 = Field(description="The UUID of the observable")

    class Config:
        orm_mode = True


class ObservableUpdate(NodeUpdate, ObservableBase):
    for_detection: Optional[StrictBool] = Field(
        description="Whether or not this observable should be included in the observable detection exports"
    )

    time: Optional[datetime] = Field(description="The time this observable was observed")

    type: Optional[type_str] = Field(description="The type of the observable")

    value: Optional[type_str] = Field(description="The value of the observable")

    _prevent_none: classmethod = validators.prevent_none("for_detection", "time", "type", "value")
