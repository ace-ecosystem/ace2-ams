from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str, validators


class ObservableTypeBase(BaseModel):
    """Represents a type of observable that the application knows about."""

    description: Optional[type_str] = Field(description="An optional human-readable description of the observable type")

    value: type_str = Field(description="The value of the observable type")


class ObservableTypeCreate(ObservableTypeBase):
    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable type")


class ObservableTypeRead(ObservableTypeBase):
    uuid: UUID4 = Field(description="The UUID of the observable type")

    class Config:
        orm_mode = True


class ObservableTypeUpdate(ObservableTypeBase):
    value: Optional[type_str] = Field(description="The value of the observable type")

    _prevent_none: classmethod = validators.prevent_none("value")
