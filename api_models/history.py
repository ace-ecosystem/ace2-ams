from datetime import datetime
from pydantic import BaseModel, Field, Json, UUID4
from typing import Optional, Union

from api_models import type_str
from api_models.event import EventRead
from api_models.observable import ObservableRead
from api_models.submission import SubmissionRead
from api_models.user import UserRead


class Diff(BaseModel):
    """Represents an individual history diff."""

    old_value: Optional[Union[type_str, bool]] = Field(description="The string value of the field prior to the action")

    new_value: Optional[Union[type_str, bool]] = Field(description="The string value of the field after to the action")

    added_to_list: list[type_str] = Field(
        description="A list of strings that were added to the field", default_factory=list
    )

    removed_from_list: list[type_str] = Field(
        description="A list of strings that were removed from the field", default_factory=list
    )


class HistoryBase(BaseModel):
    """Represents a history entry."""

    uuid: UUID4 = Field(description="The UUID of the history entry")

    action: type_str = Field(description="The action that was performed (CREATE/UPDATE/DELETE)")

    action_by: UserRead = Field(description="The user that performed the action")

    action_time: datetime = Field(description="The time the action was performed")

    record_uuid: UUID4 = Field(description="The UUID of object on which the action was performed")

    field: Optional[type_str] = Field(description="The field that was impacted by the action")

    diff: Optional[Diff] = Field(description="A JSON representation of the changes caused by the action")

    snapshot: Json = Field(description="A JSON representation of the object after the action was performed")

    class Config:
        orm_mode = True


class EventHistoryRead(HistoryBase):
    """Represents an event history entry."""

    snapshot: EventRead = Field(description="A JSON representation of the event after the action was performed")


class ObservableHistoryRead(HistoryBase):
    """Represents an observable history entry."""

    snapshot: ObservableRead = Field(
        description="A JSON representation of the observable after the action was performed"
    )


class SubmissionHistoryRead(HistoryBase):
    """Represents a submission history entry."""

    snapshot: SubmissionRead = Field(
        description="A JSON representation of the submission after the action was performed"
    )


class UserHistoryRead(HistoryBase):
    """Represents a user history entry."""

    snapshot: UserRead = Field(description="A JSON representation of the user after the action was performed")
