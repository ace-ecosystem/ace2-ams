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


def test_create_duplicate_node_uuid_value(client, db):
    alert_tree = helpers.create_alert(db=db)

    # Create a detection point
    create_json = {
        "node_uuid": str(alert_tree.node_uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client.post("/api/node/detection_point/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED

    # Make sure you cannot add the same detection point value to a node
    create_json = {
        "node_uuid": str(alert_tree.node_uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client.post("/api/node/detection_point/", json=[create_json])
    assert create.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client, db, key):
    alert_tree = helpers.create_alert(db=db)

    # Create a detection point
    create1_json = {
        "node_uuid": str(alert_tree.node_uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    client.post("/api/node/detection_point/", json=[create1_json])

    # Ensure you cannot create another detection point with the same unique field value
    create2_json = {
        "node_uuid": str(alert_tree.node_uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test2",
    }
    create2_json[key] = create1_json[key]
    create2 = client.post("/api/node/detection_point/", json=[create2_json])
    assert create2.status_code == status.HTTP_409_CONFLICT


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
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test_value", parent_tree=alert_tree, db=db)

    # Add a detection point to the node
    create_json = [
        {"node_uuid": str(observable_tree.node_uuid), "value": "test"},
    ]
    create = client.post("/api/node/detection_point/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history record
    history = client.get(f"/api/observable/{observable_tree.node_uuid}/history")
    assert history.json()["total"] == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(observable_tree.node_uuid)
    assert history.json()["items"][1]["field"] == "detection_points"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == ["test"]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["value"] == "test_value"


def test_create_multiple(client, db):
    alert_tree1 = helpers.create_alert(db=db)
    obs_tree1 = helpers.create_observable(type="test_type", value="test_value1", parent_tree=alert_tree1, db=db)
    initial_alert1_version = alert_tree1.node.version
    initial_obs1_version = obs_tree1.node.version

    alert_tree2 = helpers.create_alert(db=db)
    obs_tree2 = helpers.create_observable(type="test_type", value="test_value2", parent_tree=alert_tree2, db=db)
    initial_alert2_version = alert_tree2.node.version
    initial_obs2_version = obs_tree2.node.version

    alert_tree3 = helpers.create_alert(db=db)
    obs_tree3 = helpers.create_observable(type="test_type", value="test_value3", parent_tree=alert_tree3, db=db)
    initial_alert3_version = alert_tree3.node.version
    initial_obs3_version = obs_tree3.node.version

    assert obs_tree1.node.detection_points == []
    assert obs_tree2.node.detection_points == []
    assert obs_tree3.node.detection_points == []

    # Add a detection point to each observable at once
    create_json = [
        {"node_uuid": str(obs_tree1.node_uuid), "value": "test1"},
        {"node_uuid": str(obs_tree2.node_uuid), "value": "test2"},
        {"node_uuid": str(obs_tree3.node_uuid), "value": "test3"},
    ]
    create = client.post("/api/node/detection_point/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # The observables should each have a detection point and a new version.
    # The alerts (the root nodes) should also have a new version.
    assert len(obs_tree1.node.detection_points) == 1
    assert obs_tree1.node.detection_points[0].value == "test1"
    assert obs_tree1.node.version != initial_obs1_version
    assert alert_tree1.node.version != initial_alert1_version

    assert len(obs_tree2.node.detection_points) == 1
    assert obs_tree2.node.detection_points[0].value == "test2"
    assert obs_tree2.node.version != initial_obs2_version
    assert alert_tree2.node.version != initial_alert2_version

    assert len(obs_tree3.node.detection_points) == 1
    assert obs_tree3.node.detection_points[0].value == "test3"
    assert obs_tree3.node.version != initial_obs3_version
    assert alert_tree3.node.version != initial_alert3_version


def test_create_valid_required_fields(client, db):
    alert_tree = helpers.create_alert(db=db)
    initial_node_version = alert_tree.node.version

    # Create a detection point
    create_json = {
        "node_uuid": str(alert_tree.node_uuid),
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    create = client.post("/api/node/detection_point/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED
    assert len(alert_tree.node.detection_points) == 1
    assert alert_tree.node.detection_points[0].value == "test"
    assert alert_tree.node.version != initial_node_version
