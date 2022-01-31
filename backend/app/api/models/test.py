from pydantic import BaseModel, Field


class AddTestAlert(BaseModel):
    template: str = Field(description="The name of the alert template inside of backend/app/tests/alerts/ to insert")

    count: int = Field(description="The number of copies of the alert template to insert")
