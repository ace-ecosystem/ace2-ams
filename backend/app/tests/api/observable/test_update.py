import pytest
import uuid

from datetime import datetime
from dateutil.parser import parse
from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("expires_on", ""),
        ("expires_on", "Monday"),
        ("expires_on", "2022-01-01"),
        ("for_detection", 123),
        ("for_detection", None),
        ("for_detection", "True"),
        ("type", 123),
        ("type", None),
        ("type", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/observable/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/observable/1", json={"types": ["test_type"], "value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_type_value(client_valid_access_token, db):
    # Create some observables
    obj1 = helpers.create_observable(type="test_type", value="test", db=db)
    obj2 = helpers.create_observable(type="test_type", value="test2", db=db)

    # Ensure you cannot update an observable to have a duplicate type+value combination
    update = client_valid_access_token.patch(f"/api/observable/{obj2.uuid}", json={"value": obj1.value})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(
        f"/api/observable/{uuid.uuid4()}", json={"type": "test_type", "value": "test"}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_valid_type(client_valid_access_token, db):
    # Create the object
    obj = helpers.create_observable(type="test_type", value="test", db=db)
    assert obj.type.value == "test_type"

    # Create a new observable type
    helpers.create_observable_type(value="test_type2", db=db)

    # Update it
    update = client_valid_access_token.patch(f"/api/observable/{obj.uuid}", json={"type": "test_type2"})
    assert update.status_code == status.HTTP_204_NO_CONTENT
    assert obj.type.value == "test_type2"


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("expires_on", 1640995200, 1640995200),
        ("expires_on", None, 1640995200),
        ("expires_on", None, "2022-01-01T00:00:00Z"),
        ("expires_on", None, "2022-01-01 00:00:00"),
        ("expires_on", None, "2022-01-01 00:00:00.000000"),
        ("expires_on", None, "2021-12-31 19:00:00-05:00"),
        ("expires_on", 1640995200, None),
        ("for_detection", True, False),
        ("for_detection", True, True),
        ("value", "test", "test2"),
        ("value", "test", "test"),
    ],
)
def test_update(client_valid_access_token, db, key, initial_value, updated_value):
    # Create the object
    obj = helpers.create_observable(type="test_type", value="test", db=db)

    # Set the initial value
    if key == "expires_on" and initial_value:
        setattr(obj, key, datetime.utcfromtimestamp(initial_value))
    else:
        setattr(obj, key, initial_value)

    # Update it
    update = client_valid_access_token.patch(f"/api/observable/{obj.uuid}", json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if key == "expires_on" and updated_value:
        assert obj.expires_on == parse("2022-01-01T00:00:00+00:00")
    else:
        assert getattr(obj, key) == updated_value
