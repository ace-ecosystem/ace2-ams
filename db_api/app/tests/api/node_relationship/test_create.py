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
        ("node_uuid"),
        ("related_node_uuid"),
        ("type"),
    ],
)
def test_create_missing_required_fields(client, db, key):
    # Create two nodes
    alert1 = factory.alert.create(db=db)
    alert2 = factory.alert.create(db=db)

    # Create some node relationship types
    factory.node_relationship_type.create_or_read(value="test_rel", db=db)
    factory.node_relationship_type.create_or_read(value="test_rel2", db=db)

    # Create a node relationship
    create_json = {
        "node_uuid": str(alert1.uuid),
        "related_node_uuid": str(alert2.uuid),
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
    alert1 = factory.alert.create(db=db)
    alert2 = factory.alert.create(db=db)

    # Create a node relationship type
    factory.node_relationship_type.create_or_read(value="test_rel", db=db)

    # Create a node relationship
    create_json = {"node_uuid": str(alert1.uuid), "related_node_uuid": str(alert2.uuid), "type": "test_rel", key: value}

    # Create the object
    create = client.post("/api/node/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    # Create two nodes
    alert1 = factory.alert.create(db=db)
    alert2 = factory.alert.create(db=db)

    # Create a node relationship type
    factory.node_relationship_type.create_or_read(value="test_rel", db=db)

    # Create a node relationship
    create_json = {
        "node_uuid": str(alert1.uuid),
        "related_node_uuid": str(alert2.uuid),
        "type": "test_rel",
    }

    create = client.post("/api/node/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["node_uuid"] == str(alert1.uuid)
    assert get.json()["related_node"]["uuid"] == str(alert2.uuid)
    assert get.json()["type"]["value"] == "test_rel"


def test_create_verify_observable(client, db):
    # Create some nodes with relationships
    #
    # alert
    #   o1
    #   o2 - IS_HASH_OF o1
    alert = factory.alert.create(db=db, history_username="analyst")
    obs1 = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    obs2 = factory.observable.create_or_read(
        type="test_type", value="test_value2", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    initial_version = obs2.version
    factory.node_relationship_type.create_or_read(value="IS_HASH_OF", db=db)

    # Create the node relationship
    create_json = {
        "node_uuid": str(obs2.uuid),
        "related_node_uuid": str(obs1.uuid),
        "type": "IS_HASH_OF",
        "history_username": "analyst",
    }

    create = client.post("/api/node/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Adding a relationship counts as modifying the node, so it should have a new version
    assert obs2.version != initial_version

    # Verify the observable history. The first record is for creating the observable, and
    # the second record is from adding the node relationship.
    history = client.get(f"/api/observable/{obs2.uuid}/history")
    assert len(history.json()["items"]) == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(obs2.uuid)
    assert history.json()["items"][1]["field"] == "relationships"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == [str(obs1.uuid)]
    assert history.json()["items"][1]["diff"]["removed_from_list"] == []
    print(history.json()["items"][1])
    assert history.json()["items"][1]["snapshot"]["observable_relationships"][0]["related_node"]["uuid"] == str(
        obs1.uuid
    )
