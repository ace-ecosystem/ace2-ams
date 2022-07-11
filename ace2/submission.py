import datetime
from pydantic import Field

from .analysis import Analysis

class Submission(Analysis):
    ''' Base submission class '''

    event_time: datetime.datetime = Field(
        default_factory = datetime.datetime.utcnow,
        description = 'time in utc of the event being submitted',
    )

    mode: str = Field(default='detect', description='the current analyis mode')
    detect_mode: str = Field(description='determines which modules to run in detect mode')
    alert_mode: str = Field(description='determines which modules to run in alert mode')
    response_mode: str = Field

    queue: str = Field(description='the alert queue to display the submission in')
