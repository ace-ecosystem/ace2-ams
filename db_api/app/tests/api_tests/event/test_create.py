import pytest
import uuid

from fastapi import status

from tests.api_tests.node import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
from tests import factory


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
        ("queue", 123),
        ("queue", None),
        ("queue", ""),
        ("remediation_time", ""),
        ("remediation_time", "Monday"),
        ("remediation_time", "2022-01-01"),
        ("remediations", None),
        ("remediations", "test_type"),
        ("remediations", [123]),
        ("remediations", [None]),
        ("remediations", [""]),
        ("remediations", ["abc", 123]),
        ("severity", 123),
        ("severity", ""),
        ("source", 123),
        ("source", ""),
        ("status", 123),
        ("status", None),
        ("status", ""),
        ("type", 123),
        ("type", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("vectors", None),
        ("vectors", "test_type"),
        ("vectors", [123]),
        ("vectors", [None]),
        ("vectors", [""]),
        ("vectors", ["abc", 123]),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"name": "test", "status": "OPEN", key: value}
    create = client.post("/api/event/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in create.text


@pytest.mark.parametrize(
    "key,values",
    [
        ("tags", INVALID_LIST_STRING_VALUES),
        ("threat_actors", INVALID_LIST_STRING_VALUES),
        ("threats", INVALID_LIST_STRING_VALUES),
    ],
)
def test_create_invalid_node_fields(client, key, values):
    for value in values:
        create = client.post("/api/event/", json={key: value, "name": "test", "queue": "external", "status": "OPEN"})
        assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in create.json()["detail"][0]["loc"]


def test_create_nonexistent_owner(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post(
        "/api/event/", json={"owner": "johndoe", "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "user" in create.text


def test_create_nonexistent_prevention_tools(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post(
        "/api/event/", json={"prevention_tools": ["test"], "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_prevention_tool" in create.text


def test_create_nonexistent_queue(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post("/api/event/", json={"name": "test", "queue": "nonexistent_queue", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "queue" in create.text


def test_create_nonexistent_remediations(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post(
        "/api/event/", json={"remediations": ["test"], "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_remediation" in create.text


def test_create_nonexistent_severity(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post(
        "/api/event/", json={"severity": "test", "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_severity" in create.text


def test_create_nonexistent_source(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post("/api/event/", json={"source": "test", "name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_source" in create.text


def test_create_nonexistent_status(client, db):
    factory.queue.create_or_read(value="external", db=db)

    # Create an object
    create = client.post("/api/event/", json={"name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_status" in create.text


def test_create_nonexistent_type(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post("/api/event/", json={"type": "test", "name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_type" in create.text


def test_create_nonexistent_vectors(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create an object
    create = client.post(
        "/api/event/", json={"vectors": ["test"], "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "event_vector" in create.text


@pytest.mark.parametrize(
    "key",
    [("tags"), ("threat_actors"), ("threats")],
)
def test_create_nonexistent_node_fields(client, db, key):
    factory.event_status.create_or_read(value="OPEN", db=db)

    create = client.post("/api/event/", json={key: ["abc"], "name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in create.text


#
# VALID TESTS
#


def test_create_verify_history(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    event_uuid = str(uuid.uuid4())
    create = client.post(
        "/api/event/",
        json={"uuid": event_uuid, "name": "test", "queue": "external", "status": "OPEN", "history_username": "analyst"},
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/event/{event_uuid}/history")
    assert history.json()["total"] == 1
    assert history.json()["items"][0]["action"] == "CREATE"
    assert history.json()["items"][0]["action_by"]["username"] == "analyst"
    assert str(history.json()["items"][0]["record_uuid"]) == event_uuid
    assert history.json()["items"][0]["field"] is None
    assert history.json()["items"][0]["diff"] is None
    assert history.json()["items"][0]["snapshot"]["name"] == "test"


@pytest.mark.parametrize(
    "key,value",
    [
        ("alert_time", None),
        ("alert_time", 1640995200),
        ("alert_time", "2022-01-01T00:00:00Z"),
        ("alert_time", "2022-01-01 00:00:00"),
        ("alert_time", "2022-01-01 00:00:00.000000"),
        ("alert_time", "2021-12-31 19:00:00-05:00"),
        ("contain_time", None),
        ("contain_time", 1640995200),
        ("contain_time", "2022-01-01T00:00:00Z"),
        ("contain_time", "2022-01-01 00:00:00"),
        ("contain_time", "2022-01-01 00:00:00.000000"),
        ("contain_time", "2021-12-31 19:00:00-05:00"),
        ("disposition_time", None),
        ("disposition_time", 1640995200),
        ("disposition_time", "2022-01-01T00:00:00Z"),
        ("disposition_time", "2022-01-01 00:00:00"),
        ("disposition_time", "2022-01-01 00:00:00.000000"),
        ("disposition_time", "2021-12-31 19:00:00-05:00"),
        ("event_time", None),
        ("event_time", 1640995200),
        ("event_time", "2022-01-01T00:00:00Z"),
        ("event_time", "2022-01-01 00:00:00"),
        ("event_time", "2022-01-01 00:00:00.000000"),
        ("event_time", "2021-12-31 19:00:00-05:00"),
        ("ownership_time", None),
        ("ownership_time", 1640995200),
        ("ownership_time", "2022-01-01T00:00:00Z"),
        ("ownership_time", "2022-01-01 00:00:00"),
        ("ownership_time", "2022-01-01 00:00:00.000000"),
        ("ownership_time", "2021-12-31 19:00:00-05:00"),
        ("remediation_time", None),
        ("remediation_time", 1640995200),
        ("remediation_time", "2022-01-01T00:00:00Z"),
        ("remediation_time", "2022-01-01 00:00:00"),
        ("remediation_time", "2022-01-01 00:00:00.000000"),
        ("remediation_time", "2021-12-31 19:00:00-05:00"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client, db, key, value):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create the object
    create = client.post("/api/event/", json={key: value, "name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for one of the times, make sure that the retrieved value matches the proper UTC timestamp
    if key.endswith("_time") and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_owner(client, db):
    factory.user.create_or_read(username="johndoe", db=db)
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Use the user to create a new event
    create = client.post(
        "/api/event/", json={"owner": "johndoe", "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["owner"]["username"] == "johndoe"


def test_create_valid_prevention_tools(client, db):
    factory.event_prevention_tool.create_or_read(value="test", db=db)
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Use the prevention tool to create a new event
    create = client.post(
        "/api/event/", json={"prevention_tools": ["test"], "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["prevention_tools"][0]["value"] == "test"


def test_create_valid_remediations(client, db):
    factory.event_remediation.create_or_read(value="test", db=db)
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Use the remediation to create a new event
    create = client.post(
        "/api/event/", json={"remediations": ["test"], "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["remediations"][0]["value"] == "test"


def test_create_valid_severity(client, db):
    factory.event_severity.create_or_read(value="test", db=db)
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Use the severity to create a new event
    create = client.post(
        "/api/event/", json={"severity": "test", "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["severity"]["value"] == "test"


def test_create_valid_source(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)
    factory.event_source.create_or_read(value="test", db=db)

    # Use the source to create a new event
    create = client.post("/api/event/", json={"source": "test", "name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["source"]["value"] == "test"


def test_create_valid_type(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)
    factory.event_type.create_or_read(value="test", db=db)

    # Use the type to create a new event
    create = client.post("/api/event/", json={"type": "test", "name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["type"]["value"] == "test"


def test_create_valid_vectors(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)
    factory.event_vector.create_or_read(value="test", db=db)

    # Use the vector to create a new event
    create = client.post(
        "/api/event/", json={"vectors": ["test"], "name": "test", "queue": "external", "status": "OPEN"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["vectors"][0]["value"] == "test"


def test_create_valid_required_fields(client, db):
    factory.event_status.create_or_read(value="OPEN", db=db)

    # Create the object
    create = client.post("/api/event/", json={"name": "test", "queue": "external", "status": "OPEN"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200
    assert get.json()["name"] == "test"
    assert get.json()["status"]["value"] == "OPEN"


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("tags", VALID_LIST_STRING_VALUES, factory.node_tag.create_or_read),
        ("threat_actors", VALID_LIST_STRING_VALUES, factory.node_threat_actor.create_or_read),
        ("threats", VALID_LIST_STRING_VALUES, factory.node_threat.create_or_read),
    ],
)
def test_create_valid_node_fields(client, db, key, value_lists, helper_create_func):
    for value_list in value_lists:
        for value in value_list:
            helper_create_func(value=value, db=db)

        factory.event_status.create_or_read(value="OPEN", db=db)

        create = client.post(
            "/api/event/", json={key: value_list, "name": "test", "queue": "external", "status": "OPEN"}
        )
        assert create.status_code == status.HTTP_201_CREATED

        # Read it back
        get = client.get(create.headers["Content-Location"])
        assert len(get.json()[key]) == len(list(set(value_list)))
