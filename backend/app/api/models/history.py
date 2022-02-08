from datetime import datetime
from pydantic import BaseModel, Field, Json, UUID4
from typing import List, Optional, Union

from api.models import type_str
from api.models.alert import AlertRead
from api.models.event import EventRead
from api.models.observable import ObservableRead
from api.models.user import UserRead


class Diff(BaseModel):
    """Represents an individual history diff."""

    old_value: Optional[Union[type_str, bool]] = Field(description="The string value of the field prior to the action")

    new_value: Optional[Union[type_str, bool]] = Field(description="The string value of the field after to the action")

    added_to_list: Optional[List[type_str]] = Field(description="A list of strings that were added to the field")

    removed_from_list: Optional[List[type_str]] = Field(
        description="A list of strings that were removed from the field"
    )


class HistoryBase(BaseModel):
    """Represents a history entry."""

    uuid: UUID4 = Field(description="The UUID of the history entry")

    action: type_str = Field(description="The action that was performed (CREATE/UPDATE/DELETE)")

    action_by: type_str = Field(description="The username that performed the action")

    action_time: datetime = Field(description="The time the action was performed")

    record_uuid: UUID4 = Field(description="The UUID of object on which the action was performed")

    field: Optional[type_str] = Field(description="The field that was impacted by the action")

    diff: Optional[Diff] = Field(description="A JSON representation of the changes caused by the action")

    snapshot: Json = Field(description="A JSON representation of the object after the action was performed")

    class Config:
        orm_mode = True


class AlertHistoryRead(HistoryBase):
    """Represents an alert history entry."""

    snapshot: AlertRead = Field(description="A JSON representation of the alert after the action was performed")


class EventHistoryRead(HistoryBase):
    """Represents an event history entry."""

    snapshot: EventRead = Field(description="A JSON representation of the event after the action was performed")


class ObservableHistoryRead(HistoryBase):
    """Represents an observable history entry."""

    snapshot: ObservableRead = Field(
        description="A JSON representation of the observable after the action was performed"
    )


class UserHistoryRead(HistoryBase):
    """Represents a user history entry."""

    snapshot: UserRead = Field(description="A JSON representation of the user after the action was performed")
