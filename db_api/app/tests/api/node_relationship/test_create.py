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
        ("node_uuid", None),
        ("node_uuid", 1),
        ("node_uuid", "abc"),
        ("node_uuid", ""),
        ("related_node_uuid", None),
        ("related_node_uuid", 1),
        ("related_node_uuid", "abc"),
        ("related_node_uuid", ""),
        ("type", 123),
        ("type", None),
        ("type", ""),
        ("uuid", None),
        ("uuid", 1),
        ("uuid", "abc"),
        ("uuid", ""),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"node_uuid": str(uuid.uuid4()), "related_node_uuid": str(uuid.uuid4()), "type": "test"}
    create_json[key] = value
    create = client.post("/api/node/relationship/type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client, db, key):
    # Create two nodes
    alert_tree1 = helpers.create_alert(db=db)
    alert_tree2 = helpers.create_alert(db=db)

    # Create some node relationship types
    helpers.create_node_relationship_type(value="test_rel", db=db)
    helpers.create_node_relationship_type(value="test_rel2", db=db)

    # Create a node relationship
    create1_json = {
        "uuid": str(uuid.uuid4()),
        "node_uuid": str(alert_tree1.node_uuid),
        "related_node_uuid": str(alert_tree2.node_uuid),
        "type": "test_rel",
    }
    client.post("/api/node/relationship/", json=create1_json)

    # Ensure you cannot create another relationship with the same unique field value
    create2_json = {
        "uuid": str(uuid.uuid4()),
        "node_uuid": str(alert_tree1.node_uuid),
        "related_node_uuid": str(alert_tree2.node_uuid),
        "type": "test_rel2",
    }
    create2_json[key] = create1_json[key]
    create2 = client.post("/api/node/relationship/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("node_uuid"),
        ("related_node_uuid"),
        ("type"),
    ],
)
def test_create_missing_required_fields(client, db, key):
    # Create two nodes
    alert_tree1 = helpers.create_alert(db=db)
    alert_tree2 = helpers.create_alert(db=db)

    # Create some node relationship types
    helpers.create_node_relationship_type(value="test_rel", db=db)
    helpers.create_node_relationship_type(value="test_rel2", db=db)

    # Create a node relationship
    create_json = {
        "node_uuid": str(alert_tree1.node_uuid),
        "related_node_uuid": str(alert_tree2.node_uuid),
        "type": "test_rel",
    }

    del create_json[key]
    create = client.post("/api/node/relationship/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client, db, key, value):
    # Create two nodes
    alert_tree1 = helpers.create_alert(db=db)
    alert_tree2 = helpers.create_alert(db=db)

    # Create a node relationship type
    helpers.create_node_relationship_type(value="test_rel", db=db)

    # Create a node relationship
    create_json = {
        "node_uuid": str(alert_tree1.node_uuid),
        "related_node_uuid": str(alert_tree2.node_uuid),
        "type": "test_rel",
    }
    create_json[key] = value

    # Create the object
    create = client.post("/api/node/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    # Create two nodes
    alert_tree1 = helpers.create_alert(db=db)
    alert_tree2 = helpers.create_alert(db=db)

    # Create a node relationship type
    helpers.create_node_relationship_type(value="test_rel", db=db)

    # Create a node relationship
    create_json = {
        "node_uuid": str(alert_tree1.node_uuid),
        "related_node_uuid": str(alert_tree2.node_uuid),
        "type": "test_rel",
    }

    create = client.post("/api/node/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["node_uuid"] == str(alert_tree1.node_uuid)
    assert get.json()["related_node"]["uuid"] == str(alert_tree2.node_uuid)
    assert get.json()["type"]["value"] == "test_rel"


def test_create_verify_observable(client, db):
    # Create some nodes with relationships
    #
    # alert
    #   analysis
    #     o1
    #     o2 - IS_HASH_OF o1
    alert_tree = helpers.create_alert(db=db)
    analysis_tree = helpers.create_analysis(db=db, parent_tree=alert_tree)
    observable_tree1 = helpers.create_observable(type="test_type", value="test_value", parent_tree=analysis_tree, db=db)
    observable_tree2 = helpers.create_observable(
        type="test_type", value="test_value2", parent_tree=analysis_tree, db=db
    )
    initial_version = observable_tree2.node.version
    helpers.create_node_relationship_type(value="IS_HASH_OF", db=db)

    # Create the node relationship
    create_json = {
        "node_uuid": str(observable_tree2.node_uuid),
        "related_node_uuid": str(observable_tree1.node_uuid),
        "type": "IS_HASH_OF",
    }

    create = client.post("/api/node/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Adding a relationship counts as modifying the node, so it should have a new version
    assert observable_tree2.node.version != initial_version

    # Verify the observable history. The first record is for creating the observable, and
    # the second record is from adding the node relationship.
    history = client.get(f"/api/observable/{observable_tree2.node_uuid}/history")
    assert len(history.json()["items"]) == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(observable_tree2.node_uuid)
    assert history.json()["items"][1]["field"] == "relationships"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == [str(observable_tree1.node_uuid)]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    assert history.json()["items"][1]["snapshot"]["observable_relationships"][0]["related_node"]["uuid"] == str(
        observable_tree1.node_uuid
    )
