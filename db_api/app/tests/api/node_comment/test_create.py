import pytest
import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("node_uuid", 123),
        ("node_uuid", None),
        ("node_uuid", ""),
        ("node_uuid", "abc"),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create = client.post("/api/node/comment/", json=[{key: value, "username": "analyst"}])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_node_uuid(client):
    # Create a comment
    create_json = {
        "node_uuid": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "value": "test",
        "username": "analyst",
    }
    create = client.post("/api/node/comment/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_create_verify_history_alerts(client, db):
    alert = factory.submission.create(db=db, history_username="analyst")

    # Add a comment to the node
    create_json = [
        {"node_uuid": str(alert.uuid), "value": "test", "username": "analyst"},
    ]
    create = client.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/submission/{alert.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(alert.uuid)
    assert history.json()["items"][1]["field"] == "comments"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Alert"


def test_create_verify_history_events(client, db):
    event = factory.event.create_or_read(name="Test Event", db=db, history_username="analyst")

    # Add a comment to the node
    create_json = [
        {"node_uuid": str(event.uuid), "value": "test", "username": "analyst"},
    ]
    create = client.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/event/{event.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(event.uuid)
    assert history.json()["items"][1]["field"] == "comments"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["name"] == "Test Event"


def test_create_verify_history_observables(client, db):
    alert = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )

    # Add a comment to the node
    create_json = [
        {"node_uuid": str(observable.uuid), "value": "test", "username": "analyst"},
    ]
    create = client.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/observable/{observable.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(observable.uuid)
    assert history.json()["items"][1]["field"] == "comments"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["value"] == "test_value"


def test_create_multiple(client, db):
    alert1 = factory.submission.create(db=db)
    initial_alert1_version = alert1.version

    alert2 = factory.submission.create(db=db)
    initial_alert2_version = alert2.version

    alert3 = factory.submission.create(db=db)
    initial_alert3_version = alert3.version

    assert alert1.comments == []
    assert alert2.comments == []
    assert alert3.comments == []

    # Add a comment to each node at once
    create_json = [
        {"node_uuid": str(alert1.uuid), "value": "test1", "username": "analyst"},
        {"node_uuid": str(alert2.uuid), "value": "test2", "username": "analyst"},
        {"node_uuid": str(alert3.uuid), "value": "test3", "username": "analyst"},
    ]
    create = client.post("/api/node/comment/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    assert len(alert1.comments) == 1
    assert alert1.comments[0].value == "test1"
    assert alert1.comments[0].user.username == "analyst"
    assert alert1.version != initial_alert1_version

    assert len(alert2.comments) == 1
    assert alert2.comments[0].value == "test2"
    assert alert2.comments[0].user.username == "analyst"
    assert alert2.version != initial_alert2_version

    assert len(alert3.comments) == 1
    assert alert3.comments[0].value == "test3"
    assert alert3.comments[0].user.username == "analyst"
    assert alert3.version != initial_alert3_version


def test_create_valid_required_fields(client, db):
    alert = factory.submission.create(db=db)
    initial_node_version = alert.version

    # Create a comment
    create_json = {
        "node_uuid": str(alert.uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
        "username": "analyst",
    }
    create = client.post("/api/node/comment/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED
    assert len(alert.comments) == 1
    assert alert.comments[0].value == "test"
    assert alert.comments[0].user.username == "analyst"
    assert alert.version != initial_node_version
