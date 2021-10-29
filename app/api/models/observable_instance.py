from datetime import datetime
from pydantic import Field, UUID4
from typing import List, Optional
from uuid import uuid4

from api.models import type_str, validators
from api.models.node import NodeBase, NodeCreate, NodeRead, NodeUpdate
from api.models.observable import ObservableRead


class ObservableInstanceBase(NodeBase):
    """Represents an individual observable inside of an analysis."""

    alert_uuid: UUID4 = Field(description="The UUID of the alert containing this observable instance")

    context: Optional[type_str] = Field(
        description="""Optional context surrounding the observation. This is used to communicate additional information
            to the analysts, such as where the observation was made. For example, 'Source IP address of the sender of
            the email.' or 'From address in the email.'"""
    )

    parent_analysis_uuid: UUID4 = Field(description="The UUID of the analysis containing this observable instance")

    performed_analysis_uuids: List[UUID4] = Field(
        default_factory=list, description="A list of analysis UUIDs that were performed on this observable instance"
    )

    redirection_uuid: Optional[UUID4] = Field(
        description="The UUID of another observable instance to which this one should point"
    )

    time: datetime = Field(
        default_factory=datetime.utcnow, description="The time this observable instance was observed"
    )

    _convert_association_list: classmethod = validators.convert_association_list("performed_analysis_uuids")


class ObservableInstanceCreate(NodeCreate, ObservableInstanceBase):
    type: type_str = Field(description="The type of the observable instance")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable instance")

    value: type_str = Field(description="The value of the observable instance")


class ObservableInstanceRead(NodeRead, ObservableInstanceBase):
    observable: ObservableRead = Field(description="The observable represented by this instance")

    uuid: UUID4 = Field(description="The UUID of the observable instance")

    class Config:
        orm_mode = True


class ObservableInstanceUpdate(NodeUpdate):
    # At this point, editing an observable instance's alert_uuid and parent_analysis_uuid is not permitted.

    context: Optional[type_str] = Field(
        description="""Optional context surrounding the observation. This is used to communicate additional information
            to the analysts, such as where the observation was made. For example, 'Source IP address of the sender of
            the email.' or 'From address in the email.'"""
    )

    # UUIDs in this list will add to the existing list and will not replace it.
    performed_analysis_uuids: Optional[List[UUID4]] = Field(
        description="A list of analysis UUIDs that were performed on this observable instance"
    )

    redirection_uuid: Optional[UUID4] = Field(
        description="The UUID of another observable instance to which this one should point"
    )

    time: Optional[datetime] = Field(description="The time this observable instance was observed")

    _prevent_none: classmethod = validators.prevent_none("performed_analysis_uuids", "time")
