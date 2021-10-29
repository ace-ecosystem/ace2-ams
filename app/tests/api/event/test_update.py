import pytest
import uuid

from fastapi import status

from tests.api.node import (
    INVALID_UPDATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTOR,
    VALID_THREATS,
)


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("alert_time", ""),
        ("alert_time", "Monday"),
        ("alert_time", "2022-01-01"),
        ("contain_time", ""),
        ("contain_time", "Monday"),
        ("contain_time", "2022-01-01"),
        ("disposition_time", ""),
        ("disposition_time", "Monday"),
        ("disposition_time", "2022-01-01"),
        ("event_time", ""),
        ("event_time", "Monday"),
        ("event_time", "2022-01-01"),
        ("name", 123),
        ("name", None),
        ("name", ""),
        ("owner", 123),
        ("owner", ""),
        ("ownership_time", ""),
        ("ownership_time", "Monday"),
        ("ownership_time", "2022-01-01"),
        ("prevention_tools", None),
        ("prevention_tools", "test_type"),
        ("prevention_tools", [123]),
        ("prevention_tools", [None]),
        ("prevention_tools", [""]),
        ("prevention_tools", ["abc", 123]),
        ("remediation_time", ""),
        ("remediation_time", "Monday"),
        ("remediation_time", "2022-01-01"),
        ("remediations", None),
        ("remediations", "test_type"),
        ("remediations", [123]),
        ("remediations", [None]),
        ("remediations", [""]),
        ("remediations", ["abc", 123]),
        ("risk_level", 123),
        ("risk_level", ""),
        ("source", 123),
        ("source", ""),
        ("status", 123),
        ("status", None),
        ("status", ""),
        ("type", 123),
        ("type", ""),
        ("vectors", None),
        ("vectors", "test_type"),
        ("vectors", [123]),
        ("vectors", [None]),
        ("vectors", [""]),
        ("vectors", ["abc", 123]),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/event/{uuid.uuid4()}", json={key: value, "version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/event/{uuid.uuid4()}", json={"version": str(uuid.uuid4()), key: value}
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/event/1", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    create = client_valid_access_token.post("/api/event/", json={"name": "test", "status": "OPEN"})

    # Make sure you cannot update it using an invalid version
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key,value",
    [
        ("owner", "johndoe"),
        ("prevention_tools", ["abc"]),
        ("remediations", ["abc"]),
        ("risk_level", "abc"),
        ("source", "abc"),
        ("status", "abc"),
        ("type", "abc"),
        ("vectors", ["abc"]),
    ],
)
def test_update_nonexistent_fields(client_valid_access_token, key, value):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Make sure you cannot update it to use a nonexistent field value
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: value, "version": version})
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client_valid_access_token, key, value):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: value, "version": version})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/event/{uuid.uuid4()}", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_owner(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["owner"] is None

    # Create an alert queue
    client_valid_access_token.post("/api/alert/queue/", json={"value": "test_queue"})

    # Create a user role
    client_valid_access_token.post("/api/user/role/", json={"value": "test_role"})

    # Create a user
    create_json = {
        "default_alert_queue": "test_queue",
        "display_name": "John Doe",
        "email": "john@test.com",
        "password": "abcd1234",
        "roles": ["test_role"],
        "username": "johndoe",
    }
    client_valid_access_token.post("/api/user/", json=create_json)

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"owner": "johndoe", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["owner"]["username"] == "johndoe"
    assert get.json()["version"] != version


def test_update_prevention_tools(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["prevention_tools"] == []

    # Create an event prevention tool
    client_valid_access_token.post("/api/event/prevention_tool/", json={"value": "test"})

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"prevention_tools": ["test"], "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["prevention_tools"][0]["value"] == "test"
    assert get.json()["version"] != version


def test_update_remediations(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["remediations"] == []

    # Create an event remediation
    client_valid_access_token.post("/api/event/remediation/", json={"value": "test"})

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"remediations": ["test"], "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["remediations"][0]["value"] == "test"
    assert get.json()["version"] != version


def test_update_risk_level(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["risk_level"] is None

    # Create an event risk level
    client_valid_access_token.post("/api/event/risk_level/", json={"value": "test"})

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"risk_level": "test", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["risk_level"]["value"] == "test"
    assert get.json()["version"] != version


def test_update_source(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["source"] is None

    # Create an event source
    client_valid_access_token.post("/api/event/source/", json={"value": "test"})

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"source": "test", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["source"]["value"] == "test"
    assert get.json()["version"] != version


def test_update_status(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["status"]["value"] == "OPEN"

    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "test"})

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"status": "test", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["status"]["value"] == "test"
    assert get.json()["version"] != version


def test_update_type(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["type"] is None

    # Create an event type
    client_valid_access_token.post("/api/event/type/", json={"value": "test"})

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"type": "test", "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["type"]["value"] == "test"
    assert get.json()["version"] != version


def test_update_vectors(client_valid_access_token):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["vectors"] == []

    # Create an event vector
    client_valid_access_token.post("/api/event/vector/", json={"value": "test"})

    # Update the event
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"vectors": ["test"], "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["vectors"][0]["value"] == "test"
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client_valid_access_token, values):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/directive/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"directives": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["directives"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client_valid_access_token, values):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tags"] == []

    # Create the tags. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/tag/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"tags": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["tags"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_update_valid_node_threat_actor(client_valid_access_token, value):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["threat_actor"] is None

    # Create the threat actor
    if value:
        client_valid_access_token.post("/api/node/threat_actor/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"threat_actor": value, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    if value:
        assert get.json()["threat_actor"]["value"] == value
    else:
        assert get.json()["threat_actor"] is None

    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client_valid_access_token, values):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create an event
    version = str(uuid.uuid4())
    create = client_valid_access_token.post("/api/event/", json={"version": version, "name": "test", "status": "OPEN"})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create a threat type
    client_valid_access_token.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create the threats. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/threat/", json={"types": ["test_type"], "value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"threats": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("alert_time", "2021-01-01T00:00:00+00:00", None),
        ("alert_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("alert_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("contain_time", "2021-01-01T00:00:00+00:00", None),
        ("contain_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("contain_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", None),
        ("disposition_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("disposition_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", None),
        ("event_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("event_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", None),
        ("ownership_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("ownership_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", None),
        ("remediation_time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("remediation_time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
        ("name", "test", "test2"),
        ("name", "test", "test"),
    ],
)
def test_update(client_valid_access_token, key, initial_value, updated_value):
    # Create an event status
    client_valid_access_token.post("/api/event/status/", json={"value": "OPEN"})

    # Create the object
    version = str(uuid.uuid4())
    create_json = {"version": version, "name": "test", "status": "OPEN"}
    create_json[key] = initial_value
    create = client_valid_access_token.post("/api/event/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == initial_value

    # Update it
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"version": version, key: updated_value}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for one of the times, make sure that the retrieved value matches the proper UTC timestamp
    if key.endswith("_time") and updated_value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == updated_value

    assert get.json()["version"] != version
