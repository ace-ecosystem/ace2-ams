from pydantic import Field

from .analysis import Analysis
from .timestamp import Timestamp, now

class Submission(Analysis):
    ''' Base submission class '''

    event_time: Timestamp = Field(default_factory=now, description='time in utc of the event being submitted')

    mode: str = Field(default='detect', description='the current analyis mode')
    detect_mode: str = Field(description='determines which modules to run in detect mode')
    alert_mode: str = Field(description='determines which modules to run in alert mode')
    response_mode: str = Field(desctiption='determines which modules to run in response mode')

    queue: str = Field(description='the alert queue to display the submission in')
