from pydantic import BaseModel, Field, UUID4


class Create(BaseModel):
    """Represents a response when creating a new object."""

    uuid: UUID4 = Field(description="The UUID of the new object")
