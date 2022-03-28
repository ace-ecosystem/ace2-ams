from pydantic import BaseModel, Field, UUID4
from typing import List, Optional

from api.models import type_str
from api.models.analysis_details import (
    EmailAnalysisDetailsBase,
    EmailAnalysisDetailsHeaderBody,
    SandboxAnalysisDetails,
    UserAnalysisDetails,
)
from api.models.node_detection_point import NodeDetectionPointRead
from api.models.observable import ObservableRead


class DetectionSummary(NodeDetectionPointRead):
    """Represents an individual detection point found in an event."""

    alert_uuid: UUID4 = Field(description="An alert UUID in which this detection point was found")

    count: int = Field(description="The number of times this detection point value was found in the event")


class EmailHeadersBody(EmailAnalysisDetailsHeaderBody):
    """Represents the fields in Email Analysis details that the frontend expects for event pages."""

    alert_uuid: UUID4 = Field(description="The UUID of the alert to which this email belongs")


class EmailSummary(EmailAnalysisDetailsBase):
    """Represents the fields in Email Analysis details that the frontend expects for event pages."""

    alert_uuid: UUID4 = Field(description="The UUID of the alert to which this email belongs")


class ObservableSummary(ObservableRead):
    """Represents an observable summary as used on the event pages."""

    faqueue_hits: int = Field(description="The number of hits found by FA Queue Analysis for this observable")

    faqueue_link: Optional[type_str] = Field(description="An optional link to view the FA Queue search")


class SandboxSummary(SandboxAnalysisDetails):
    """Represents a sandbox report summary as used on the event pages."""

    alert_uuid: UUID4 = Field(description="The UUID of the alert to which this sandbox summary belongs")


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


class UserSummary(UserAnalysisDetails):
    """Represents a user summary as used on the event pages."""

    pass
