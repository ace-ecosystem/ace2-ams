import datetime
import pytest

# apply this fixture to all tests
@pytest.fixture(autouse=True)
def mock_datetime(monkeypatch):
    # create a mock mock datetime class that returns a fixed datetime
    class dt(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.datetime(2020, 1, 2, 3, 4, 5, 6, tzinfo=tz)

        @classmethod
        def utcnow(cls):
            return cls.now()

    # patch datetime so it produces fixed values
    monkeypatch.setattr('datetime.datetime', dt)

    # return the fixed datetime class so tests can make assesrtions with it
    return dt
