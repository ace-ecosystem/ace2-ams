from pydantic import BaseModel, Field

from api_models import type_str


class URLDomainSummaryIndividual(BaseModel):
    """Represents an individual URL domain summary."""

    domain: type_str = Field(description="The domain from the URL observables")

    count: int = Field(description="The number of times the domain occurred in unique URL observables")


class URLDomainSummary(BaseModel):
    """Represents a URL domain summary as used on the event and alert (submission) pages."""

    domains: list[URLDomainSummaryIndividual] = Field(description="The domain from the URL observables")

    total: int = Field(
        description="The cumulative total of all the counts. count/total gives the ratio of this domain's occurrences."
    )
