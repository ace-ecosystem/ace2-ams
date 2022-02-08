from pydantic import BaseModel, Field
from typing import Optional

from api.models import type_str

class AddTestAlert(BaseModel):
    template: str = Field(description="The name of the alert template inside of backend/app/tests/alerts/ to insert")

    count: int = Field(description="The number of copies of the alert template to insert")


class AddTestEvent(BaseModel):
    alert_template: str = Field(
        description="The name of the alert template inside of backend/app/tests/alerts/ to insert"
    )

    alert_count: int = Field(description="The number of copies of the alert template to insert")

    name: str = Field(description="The name to use for the event")

    status: Optional[type_str] = Field(description="The status to use for the event", default="OPEN")
