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
    create = client.post("/api/node/detection_point/", json=[{key: value}])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_node_uuid(client, db):
    create_json = {
        "node_uuid": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client.post("/api/node/detection_point/", json=[create_json])
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_create_verify_history_observables(client, db):
    alert = factory.submission.create(db=db, history_username="analyst")
    observable = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )

    # Add a detection point to the node
    create_json = [
        {"node_uuid": str(observable.uuid), "value": "test", "history_username": "analyst"},
    ]
    create = client.post("/api/node/detection_point/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/observable/{observable.uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(observable.uuid)
    assert history.json()["items"][1]["field"] == "detection_points"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["value"] == "test_value"


def test_create_multiple(client, db):
    alert1 = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(
        type="test_type", value="test_value1", parent_analysis=alert1.root_analysis, db=db
    )
    initial_alert1_version = alert1.version
    initial_obs1_version = obs1.version

    alert2 = factory.submission.create(db=db)
    obs2 = factory.observable.create_or_read(
        type="test_type", value="test_value2", parent_analysis=alert2.root_analysis, db=db
    )
    initial_alert2_version = alert2.version
    initial_obs2_version = obs2.version

    alert3 = factory.submission.create(db=db)
    obs3 = factory.observable.create_or_read(
        type="test_type", value="test_value3", parent_analysis=alert3.root_analysis, db=db
    )
    initial_alert3_version = alert3.version
    initial_obs3_version = obs3.version

    assert obs1.detection_points == []
    assert obs2.detection_points == []
    assert obs3.detection_points == []

    # Add a detection point to each observable at once
    create_json = [
        {"node_uuid": str(obs1.uuid), "value": "test1", "history_username": "analyst"},
        {"node_uuid": str(obs2.uuid), "value": "test2", "history_username": "analyst"},
        {"node_uuid": str(obs3.uuid), "value": "test3", "history_username": "analyst"},
    ]
    create = client.post("/api/node/detection_point/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # The observables should each have a detection point and a new version.
    # TODO: Fix The alerts (the root nodes) should also have a new version.
    assert len(obs1.detection_points) == 1
    assert obs1.detection_points[0].value == "test1"
    assert obs1.version != initial_obs1_version
    # assert alert1.version != initial_alert1_version

    assert len(obs2.detection_points) == 1
    assert obs2.detection_points[0].value == "test2"
    assert obs2.version != initial_obs2_version
    # assert alert2.version != initial_alert2_version

    assert len(obs3.detection_points) == 1
    assert obs3.detection_points[0].value == "test3"
    assert obs3.version != initial_obs3_version
    # assert alert3.version != initial_alert3_version


def test_create_valid_required_fields(client, db):
    alert = factory.submission.create(db=db)
    initial_node_version = alert.version

    # Create a detection point
    create_json = {
        "node_uuid": str(alert.uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
        "history_username": "analyst",
    }
    create = client.post("/api/node/detection_point/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED
    assert len(alert.detection_points) == 1
    assert alert.detection_points[0].value == "test"
    assert alert.version != initial_node_version
