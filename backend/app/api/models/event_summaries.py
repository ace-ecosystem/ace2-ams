from pydantic import BaseModel, Field
from typing import List, Optional

from api.models import type_str
from api.models.observable import ObservableRead


class ObservableSummary(ObservableRead):
    """Represents an observable summary as used on the event pages."""

    faqueue_hits: int = Field(description="The number of hits found by FA Queue Analysis for this observable")

    faqueue_link: str = Field(description="An optional link to view the FA Queue search")


class URLDomainSummaryIndividual(BaseModel):
    """Represents an individual URL domain summary."""

    domain: type_str = Field(description="The domain from the URL observables")

    count: int = Field(description="The number of times the domain occurred in unique URL observables")


class URLDomainSummary(BaseModel):
    """Represents a URL domain summary as used on the event pages."""

    domains: List[URLDomainSummaryIndividual] = Field(description="The domain from the URL observables")

    total: int = Field(
        description="The cumulative total of all the counts. count/total gives the ratio of this domain's occurrences."
    )


class UserSummary(BaseModel):
    """Represents a user summary as used on the event pages."""

    company: Optional[str] = Field(description="The company to which the user belongs")

    department: Optional[str] = Field(description="The department to which the user belongs")

    division: Optional[str] = Field(description="The division to which the user belongs")

    email: type_str = Field(description="The user's email address")

    manager_email: Optional[str] = Field(description="The email address of the user's manager")

    title: Optional[str] = Field(description="The user's job title")

    user_id: type_str = Field(description="The user's user ID")
