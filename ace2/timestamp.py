from __future__ import annotations
from datetime import datetime, tzinfo
from pydantic import BaseModel
from pytz import utc, timezone
from typing import Union

# timezone shorthands available for import
eastern = timezone('US/Eastern')

class Timestamp(datetime):
    ''' datetime wrapper for producing validatable utc timestamps '''

    @classmethod
    def from_datetime(cls, dt:datetime, tz:tzinfo=utc) -> Timestamp:
        ''' creates a Timestamp object from a datetime object

        Args:
            dt: the datetime to turn into a Timestamp
            tz: the timezone to use for the datetime if it does not have one

        Returns:
            Timestamp object int utc representing the same time as the given datetime
        '''

        # convert dt to utc
        if not dt.tzinfo:
            dt = tz.localize(dt)
        dt = dt.astimezone(utc)

        # cast the datetime object to a Timestamp object
        return cls(
            year = dt.year,
            month = dt.month,
            day = dt.day,
            hour = dt.hour,
            minute = dt.minute,
            second = dt.second,
            microsecond = dt.microsecond,
            tzinfo = dt.tzinfo,
            fold = dt.fold,
        )

    @classmethod
    def fromisoformat(cls, timestamp:str, tz:tzinfo=utc) -> Timestamp:
        ''' creates a Timestamp object from a iso formatted timestamp string

        Args:
            timestamp: the iso formatted string to convert to a Timestamp Object
            tz: the timezone to use for the string if it does not have one

        Returns:
            the utc Timestamp object represented by the given iso formatted timestamp string
        '''

        # create Timestamp object from iso formatted string
        return cls.from_datetime(datetime.fromisoformat(timestamp), tz)

    def isoformat(self) -> str:
        ''' isoformat function wrapper to give a consistent isoformat. (i.e. always output microsecond) '''

        # format the Timestamp as string
        s = self.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

        # add the colon between the timezone hour and minute
        return s[:-2] + ':' + s[-2:]

    @classmethod
    def strptime(cls, timestamp:str, pattern:str, tz:tzinfo=utc) -> Timestamp:
        ''' creates a Timestamp object from a formatted string defined by pattern

        Args:
            timestamp: the formatted string to convert to a Timestamp Object
            pattern: the pattern that defines the time format of the timestamp
            tz: the timezone to use for the string if it does not have one

        Returns:
            the utc Timestamp object represented by the given formatted timestamp string
        '''

        # create Timestamp object from formatted string
        return cls.from_datetime(datetime.strptime(timestamp, pattern), tz)

    @classmethod
    def now(cls) -> Timestamp:
        ''' gets the current time as a UTC Timestamp object

        Returns:
            the current time in UTC as a Timestamp object
        '''

        # create Timestamp object from current utc time
        return cls.from_datetime(datetime.utcnow())

    @classmethod
    def utcnow(cls):
        ''' gets the current time as a UTC Timestamp object

        Returns:
            the current time in UTC as a Timestamp object
        '''

        # return current time as Timestamp object
        return cls.now()

    @classmethod
    def __get_validators__(cls):
        ''' override of pydantic function to add custom validator to the class '''
        yield cls.validate

    @classmethod
    def validate(cls, value:Union[Timestamp,datetime,str]) -> Timestamp:
        ''' custom pydantic validator that converts various types to Timestamps

        Args:
            value: the value to convert

        Returns:
            the Timestamp object representing value
        '''

        # if its already a Timestamp then we are good to go
        if isinstance(value, cls):
            return value

        # convert datetime objects to Timestamp objects
        if isinstance(value, datetime):
            return cls.from_datetime(value)

        # convert strings to Timestamp objects
        if isinstance(value, str):
            # TODO: support other common string formats
            return cls.fromisoformat(value)

        raise TypeError(f"Unsupported Timestamp type: '{type(value).__name__}'")

def now() -> Timestamp:
    ''' returns the current time in UTC as a Timestamp object

    Returns:
        the current time in UTC as a Timestamp object
    '''

    # return the current time as a Timestamp object
    return Timestamp.now()

def strptime(timestamp:str, pattern:str, tz:tzinfo=utc):
    ''' creates a Timestamp object from a formatted string defined by pattern

    Args:
        timestamp: the formatted string to convert to a Timestamp Object
        pattern: the pattern that defines the format of the timestamp
        tz: the timezone to use for the string if it does not have one

    Returns:
        the utc Timestamp object represented by the given formatted timestamp string
    '''

    # create a Timestamp object that represents the given formatted timestamp string
    return Timestamp.strptime(timestamp, pattern, tz)
