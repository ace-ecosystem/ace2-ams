from datetime import datetime
from pydantic import BaseModel, Field, StrictBool, UUID4
from typing import Optional
from uuid import uuid4

from api.models import type_str, validators
from api.models.observable_type import ObservableTypeRead


class ObservableBase(BaseModel):
    """Represents a unique observable (based on the type+value)."""

    expires_on: Optional[datetime] = Field(
        description="The time the observable will expire and no longer be included in observable detection exports"
    )

    for_detection: StrictBool = Field(
        default=False,
        description="Whether or not this observable should be included in the observable detection exports",
    )

    type: type_str = Field(description="The type of the observable")

    value: type_str = Field(description="The value of the observable")


class ObservableCreate(ObservableBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable")


class ObservableRead(ObservableBase):
    type: ObservableTypeRead = Field(description="The type of the observable")

    uuid: UUID4 = Field(description="The UUID of the observable")

    class Config:
        orm_mode = True


class ObservableUpdate(ObservableBase):
    for_detection: Optional[StrictBool] = Field(
        description="Whether or not this observable should be included in the observable detection exports"
    )

    type: Optional[type_str] = Field(description="The type of the observable")

    value: Optional[type_str] = Field(description="The value of the observable")

    _prevent_none: classmethod = validators.prevent_none("for_detection", "type", "value")
