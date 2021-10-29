import pytest
import uuid

from fastapi import status

from core.auth import verify_password
from db import crud
from db.schemas.user import User


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("default_alert_queue", 123),
        ("default_alert_queue", None),
        ("default_alert_queue", ""),
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
        ("username", 123),
        ("username", None),
        ("username", ""),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/user/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/user/1", json={"value": "test"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("email"),
        ("username"),
    ],
)
def test_update_duplicate_unique_fields(client_valid_access_token, key):
    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create some objects
    create1_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client_valid_access_token.post("/api/user/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {
        "default_alert_queue": "test_queue",
        "display_name": "Jane Doe",
        "email": "jane@test.com",
        "password": "wxyz6789",
        "roles": ["test_role"],
        "username": "janedoe",
    }
    create2 = client_valid_access_token.post("/api/user/", json=create2_json)

    # Ensure you cannot update a unique field to a value that already exists
    update = client_valid_access_token.patch(create2.headers["Content-Location"], json={key: create1_json[key]})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/user/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "value",
    [
        ("new_queue"),
    ],
)
def test_update_valid_alert_queue(client_valid_access_token, value):
    # Create an initial alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "initial_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create the object
    create_json = {
        "default_alert_queue": "initial_queue",
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
    assert get.json()["default_alert_queue"]["value"] == "initial_queue"

    # Create the new alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": value})

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"default_alert_queue": value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["default_alert_queue"]["value"] == value


@pytest.mark.parametrize(
    "value",
    [
        (["new_role"]),
        (["new_role1", "new_role2"]),
    ],
)
def test_update_valid_roles(client_valid_access_token, value):
    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create some user roles
    initial_roles = ["test_role1", "test_role2", "test_role3"]
    for role in initial_roles:
        client_valid_access_token.post("/api/user/role/", json={"value": role})

    # Create the object
    create1_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": initial_roles,
        "username": "johndoe",
    }
    create = client_valid_access_token.post("/api/user/", json=create1_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["roles"]) == len(initial_roles)

    # Create the new user roles
    for role in value:
        client_valid_access_token.post("/api/user/role/", json={"value": role})

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"roles": value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["roles"]) == len(value)


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("display_name", "John Doe", "Johnathan Doe"),
        ("display_name", "John Doe", "John Doe"),
        ("email", "john@test.com", "johnathan@test.com"),
        ("email", "john@test.com", "john@test.com"),
        ("enabled", True, False),
        ("enabled", False, True),
        ("timezone", "UTC", "America/New_York"),
        ("timezone", "UTC", "UTC"),
        ("username", "johndoe", "johnathandoe"),
        ("username", "johndoe", "johndoe"),
    ],
)
def test_update(client_valid_access_token, key, initial_value, updated_value):
    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create the object
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "timezone": "America/New_York",
        "username": "johndoe",
    }
    create_json[key] = initial_value
    create = client_valid_access_token.post("/api/user/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == initial_value

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == updated_value


@pytest.mark.parametrize(
    "initial_value,updated_value",
    [
        ("abcd1234", "wxyz6789"),
        ("abcd1234", "abcd1234"),
    ],
)
def test_update_password(client_valid_access_token, db, initial_value, updated_value):
    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create the object
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": initial_value,
        "roles": ["test_role"],
        "username": "johndoe",
    }
    create = client_valid_access_token.post("/api/user/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back to get the UUID
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # Manually retrieve the user from the database so we have the initial password hash
    initial_user = crud.read(uuid=get.json()["uuid"], db_table=User, db=db)
    initial_hash = initial_user.password

    # Make sure the initial password validates against its hash
    assert verify_password(initial_value, initial_hash) is True

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"password": updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Manually retrieve the user from the database so we have the updated password hash
    updated_user = crud.read(uuid=get.json()["uuid"], db_table=User, db=db)
    updated_hash = updated_user.password

    # Make sure the two hashes are not the same
    assert initial_hash != updated_hash

    # Make sure the updated password validates against its hash
    assert verify_password(updated_value, updated_hash) is True
