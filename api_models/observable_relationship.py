from pydantic import BaseModel, Field, UUID4
from typing import Optional
from uuid import uuid4

from api_models import type_str
from api_models.observable_relationship_type import ObservableRelationshipTypeRead


class ObservableRelationshipBase(BaseModel):
    """Represents a relationship that can be applied to an observable."""

    observable_uuid: UUID4 = Field(description="The UUID of the observable")


class ObservableRelationshipCreate(ObservableRelationshipBase):
    history_username: Optional[type_str] = Field(
        description="If given, a history record will be created and associated with the user"
    )

    related_observable_uuid: UUID4 = Field(description="The UUID of the related observable")

    type: type_str = Field(description="The type of the observable relationship")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the observable relationship")


class ObservableRelationshipRead(ObservableRelationshipBase):
    uuid: UUID4 = Field(description="The UUID of the observable relationship")

    related_observable: "ObservableRead" = Field(description="The related observable")

    type: ObservableRelationshipTypeRead = Field(description="The type of the observable relationship")

    class Config:
        orm_mode = True


from api_models.observable import ObservableRead

ObservableRelationshipRead.update_forward_refs()
