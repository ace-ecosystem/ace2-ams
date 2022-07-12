from ace2 import *
from datetime import datetime
from pydantic import BaseModel
import pytest


def test_timestamp(mock_now):
    dt = datetime(2022, 7, 12, 10, 0, 0, 0)
    edt = eastern.localize(datetime(2022, 7, 12, 10, 0, 0, 0))

    # test from_datetime with no timezone
    timestamp = Timestamp.from_datetime(dt)
    assert timestamp.isoformat() == '2022-07-12T10:00:00.000000+00:00'
    
    # test from_datetime with eastern timezone
    timestamp = Timestamp.from_datetime(dt, eastern)
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'

    # test on dt with a timezone
    timestamp = Timestamp.from_datetime(edt)
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'


    # test fromisoformat with no timezone
    timestamp = Timestamp.fromisoformat('2022-07-12T10:00:00')
    assert timestamp.isoformat() == '2022-07-12T10:00:00.000000+00:00'

    # test fromisoformat with eastern timezone
    timestamp = Timestamp.fromisoformat('2022-07-12T10:00:00', eastern)
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'

    # test fromisoformat with timezone in string
    timestamp = Timestamp.fromisoformat('2022-07-12T10:00:00-04:00')
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'


    # test strptime with no timezone
    timestamp = Timestamp.strptime('2022-07-12T10:00:00', '%Y-%m-%dT%H:%M:%S')
    assert timestamp.isoformat() == '2022-07-12T10:00:00.000000+00:00'
    timestamp = strptime('2022-07-12T10:00:00', '%Y-%m-%dT%H:%M:%S')
    assert timestamp.isoformat() == '2022-07-12T10:00:00.000000+00:00'

    # test strptime with eastern timezone
    timestamp = Timestamp.strptime('2022-07-12T10:00:00', '%Y-%m-%dT%H:%M:%S', eastern)
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'
    timestamp = strptime('2022-07-12T10:00:00', '%Y-%m-%dT%H:%M:%S', eastern)
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'

    # test strptime with timezone in string
    timestamp = Timestamp.strptime('2022-07-12T10:00:00-04:00', '%Y-%m-%dT%H:%M:%S%z')
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'
    timestamp = strptime('2022-07-12T10:00:00-04:00', '%Y-%m-%dT%H:%M:%S%z')
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'


    # test now functions
    assert now() == mock_now
    assert Timestamp.now() == mock_now
    assert Timestamp.utcnow() == mock_now


    # create a class to test the pydantic validator with
    class Model(BaseModel):
        dt: Timestamp

    # test validator with Timestamp
    m = Model(dt=now())
    assert m.dt == mock_now

    # test validator with iso formatted string
    m = Model(dt='2022-07-12T10:00:00')
    assert m.dt.isoformat() == '2022-07-12T10:00:00.000000+00:00'
