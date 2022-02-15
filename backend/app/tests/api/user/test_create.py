import pytest
import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("default_alert_queue", 123),
        ("default_alert_queue", None),
        ("default_alert_queue", ""),
        ("default_event_queue", 123),
        ("default_event_queue", None),
        ("default_event_queue", ""),
        ("display_name", 123),
        ("display_name", None),
        ("display_name", ""),
        ("email", 123),
        ("email", None),
        ("email", ""),
        ("email", "johndoe"),
        ("email", "johndoe@test"),
        ("enabled", 123),
        ("enabled", None),
        ("enabled", "True"),
        ("password", 123),
        ("password", None),
        ("password", ""),
        ("password", "abc"),
        ("roles", 123),
        ("roles", None),
        ("roles", "test_role"),
        ("roles", [123]),
        ("roles", [None]),
        ("roles", [""]),
        ("roles", ["abc", 123]),
        ("timezone", 123),
        ("timezone", None),
        ("timezone", ""),
        ("timezone", "Mars/Jezero"),
        ("training", 123),
        ("training", None),
        ("training", "True"),
        ("username", 123),
        ("username", None),
        ("username", ""),
        ("uuid", None),
        ("uuid", 1),
        ("uuid", "abc"),
        ("uuid", ""),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {
        "default_alert_queue": "test_queue",
        "default_event_queue": "test_queue",
        "display_name": "John Doe",
        "email": "johndoe@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/user/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("email"),
        ("username"),
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, db, key):
    helpers.create_alert_queue(value="test_queue", db=db)
    helpers.create_event_queue(value="test_queue", db=db)
    helpers.create_user_role(value="test_role", db=db)

    # Create an object
    create1_json = {
        "default_alert_queue": "test_queue",
        "default_event_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
        "uuid": str(uuid.uuid4()),
    }
    client_valid_access_token.post("/api/user/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {
        "default_alert_queue": "test_queue",
        "default_event_queue": "test_queue",
        "display_name": "Jane Doe",
        "email": "jane@test.com",
        "password": "wxyz6789",
        "roles": ["test_role"],
        "username": "janedoe",
        "uuid": str(uuid.uuid4()),
    }
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/user/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("default_alert_queue"),
        ("default_event_queue"),
        ("display_name"),
        ("email"),
        ("password"),
        ("roles"),
        ("username"),
    ],
)
def test_create_missing_required_fields(client_valid_access_token, key):
    create_json = {
        "default_alert_queue": "test_queue",
        "default_event_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    del create_json[key]
    create = client_valid_access_token.post("/api/user/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# VALID TESTS
#


def test_create_verify_history(client_valid_access_token, db):
    helpers.create_alert_queue(value="test_queue", db=db)
    helpers.create_event_queue(value="test_queue", db=db)
    helpers.create_user_role(value="test_role", db=db)

    # Create the object
    user_uuid = str(uuid.uuid4())
    create_json = {
        "default_alert_queue": "test_queue",
        "default_event_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
        "uuid": user_uuid,
    }
    create = client_valid_access_token.post("/api/user/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client_valid_access_token.get(f"/api/user/{user_uuid}/history")
    assert history.json()["total"] == 1
    assert history.json()["items"][0]["action"] == "CREATE"
    assert history.json()["items"][0]["action_by"]["username"] == "analyst"
    assert history.json()["items"][0]["record_uuid"] == user_uuid
    assert history.json()["items"][0]["field"] is None
    assert history.json()["items"][0]["diff"] is None
    assert history.json()["items"][0]["snapshot"]["username"] == "johndoe"


@pytest.mark.parametrize(
    "key,value",
    [("enabled", False), ("timezone", "America/New_York"), ("training", False), ("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client_valid_access_token, db, key, value):
    helpers.create_alert_queue(value="test_queue", db=db)
    helpers.create_event_queue(value="test_queue", db=db)
    helpers.create_user_role(value="test_role", db=db)

    # Create the object
    create_json = {
        "default_alert_queue": "test_queue",
        "default_event_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/user/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client_valid_access_token, db):
    helpers.create_alert_queue(value="test_queue", db=db)
    helpers.create_event_queue(value="test_queue", db=db)
    helpers.create_user_role(value="test_role", db=db)

    # Create the object
    create_json = {
        "default_alert_queue": "test_queue",
        "default_event_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    create = client_valid_access_token.post("/api/user/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["default_alert_queue"]["value"] == "test_queue"
    assert get.json()["default_event_queue"]["value"] == "test_queue"
    assert get.json()["display_name"] == "John Doe"
    assert get.json()["email"] == "john@test.com"
    assert get.json()["enabled"] is True
    assert "password" not in get.json()
    assert len(get.json()["roles"]) == 1
    assert get.json()["roles"][0]["value"] == "test_role"
    assert get.json()["timezone"] == "UTC"
    assert get.json()["training"] is True
    assert get.json()["username"] == "johndoe"
