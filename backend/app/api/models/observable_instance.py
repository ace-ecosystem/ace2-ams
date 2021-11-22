from datetime import datetime
from pydantic import Field, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators
from api.models.node import NodeBase, NodeCreate, NodeRead, NodeUpdate
from api.models.observable import ObservableRead


class ObservableInstanceBase(NodeBase):
    """Represents an individual observable inside of an analysis."""

    context: Optional[type_str] = Field(
        description="""Optional context surrounding the observation. This is used to communicate additional information
            to the analysts, such as where the observation was made. For example, 'Source IP address of the sender of
            the email.' or 'From address in the email.'"""
    )

    redirection_uuid: Optional[UUID4] = Field(
        description="The UUID of another observable instance to which this one should point"
    )

    time: datetime = Field(
        default_factory=datetime.utcnow, description="The time this observable instance was observed"
    )


class ObservableInstanceCreateBase(NodeCreate, ObservableInstanceBase):
    type: type_str = Field(description="The type of the observable instance")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable instance")

    value: type_str = Field(description="The value of the observable instance")


class ObservableInstanceCreate(ObservableInstanceCreateBase):
    alert_uuid: UUID4 = Field(description="The UUID of the alert containing this observable instance")

    parent_uuid: UUID4 = Field(description="The UUID of the analysis containing this observable instance")


class ObservableInstanceCreateWithAlert(ObservableInstanceCreateBase):
    pass


class ObservableInstanceRead(NodeRead, ObservableInstanceBase):
    alert_uuid: UUID4 = Field(description="The UUID of the alert containing this observable instance")

    observable: ObservableRead = Field(description="The observable represented by this instance")

    parent_uuid: UUID4 = Field(description="The UUID of the analysis containing this observable instance")

    uuid: UUID4 = Field(description="The UUID of the observable instance")

    class Config:
        orm_mode = True


class ObservableInstanceUpdate(NodeUpdate):
    # At this point, editing an observable instance's alert_uuid and parent_uuid is not permitted.

    context: Optional[type_str] = Field(
        description="""Optional context surrounding the observation. This is used to communicate additional information
            to the analysts, such as where the observation was made. For example, 'Source IP address of the sender of
            the email.' or 'From address in the email.'"""
    )

    redirection_uuid: Optional[UUID4] = Field(
        description="The UUID of another observable instance to which this one should point"
    )

    time: Optional[datetime] = Field(description="The time this observable instance was observed")

    _prevent_none: classmethod = validators.prevent_none("time")
