from ace2 import *
from datetime import datetime

def test_timestamp_from_datetime():
    dt = datetime(2022, 7, 12, 10, 0, 0, 0)
    timestamp = Timestamp.from_datetime(dt)
    assert timestamp.isoformat() == '2022-07-12T10:00:00.000000+00:00'
    
    timestamp = Timestamp.from_datetime(dt, eastern)
    assert timestamp.isoformat() == '2022-07-12T14:00:00.000000+00:00'
