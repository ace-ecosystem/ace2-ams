from pydantic import Field
from typing import Optional

from api.models import type_str
from api.models.observable import ObservableRead


class ObservableSummary(ObservableRead):
    """Represents an event's observable summary."""

    faqueue_hits: int = Field(description="The number of hits found by FA Queue Analysis for this observable")

    faqueue_link: Optional[type_str] = Field(description="An optional link to view the FA Queue search")
