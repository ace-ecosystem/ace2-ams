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
        ("observable_uuid", None),
        ("observable_uuid", 1),
        ("observable_uuid", "abc"),
        ("observable_uuid", ""),
        ("related_observable_uuid", None),
        ("related_observable_uuid", 1),
        ("related_observable_uuid", "abc"),
        ("related_observable_uuid", ""),
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
    create_json = {"observable_uuid": str(uuid.uuid4()), "related_observable_uuid": str(uuid.uuid4()), "type": "test"}
    create_json[key] = value
    create = client.post("/api/observable/relationship/type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("observable_uuid"),
        ("related_observable_uuid"),
        ("type"),
    ],
)
def test_create_missing_required_fields(client, db, key):
    alert = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert.root_analysis, db=db)
    obs2 = factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert.root_analysis, db=db)

    # Create some observable relationship types
    factory.observable_relationship_type.create_or_read(value="test_rel", db=db)
    factory.observable_relationship_type.create_or_read(value="test_rel2", db=db)

    # Create a observable relationship
    create_json = {
        "observable_uuid": str(obs1.uuid),
        "related_observable_uuid": str(obs2.uuid),
        "type": "test_rel",
    }

    del create_json[key]
    create = client.post("/api/observable/relationship/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [("uuid", str(uuid.uuid4()))],
)
def test_create_valid_optional_fields(client, db, key, value):
    alert = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert.root_analysis, db=db)
    obs2 = factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert.root_analysis, db=db)

    # Create a observable relationship type
    factory.observable_relationship_type.create_or_read(value="test_rel", db=db)

    # Create a observable relationship
    create_json = {
        "observable_uuid": str(obs1.uuid),
        "related_observable_uuid": str(obs2.uuid),
        "type": "test_rel",
        key: value,
    }

    # Create the object
    create = client.post("/api/observable/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    alert = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert.root_analysis, db=db)
    obs2 = factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert.root_analysis, db=db)

    # Create a observable relationship type
    factory.observable_relationship_type.create_or_read(value="test_rel", db=db)

    # Create a observable relationship
    create_json = {
        "observable_uuid": str(obs1.uuid),
        "related_observable_uuid": str(obs2.uuid),
        "type": "test_rel",
    }

    create = client.post("/api/observable/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["observable_uuid"] == str(obs1.uuid)
    assert get.json()["related_observable"]["uuid"] == str(obs2.uuid)
    assert get.json()["type"]["value"] == "test_rel"


def test_create_verify_observable(client, db):
    # Create some observables with relationships
    #
    # alert
    #   o1
    #   o2 - IS_HASH_OF o1
    alert = factory.submission.create(db=db, history_username="analyst")
    obs1 = factory.observable.create_or_read(
        type="test_type", value="test_value", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    obs2 = factory.observable.create_or_read(
        type="test_type", value="test_value2", parent_analysis=alert.root_analysis, db=db, history_username="analyst"
    )
    initial_version = obs2.version
    factory.observable_relationship_type.create_or_read(value="IS_HASH_OF", db=db)

    # Create the observable relationship
    create_json = {
        "observable_uuid": str(obs2.uuid),
        "related_observable_uuid": str(obs1.uuid),
        "type": "IS_HASH_OF",
        "history_username": "analyst",
    }

    create = client.post("/api/observable/relationship/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Adding a relationship counts as modifying the observable, so it should have a new version
    assert obs2.version != initial_version

    # Verify the observable history. The first record is for creating the observable, and
    # the second record is from adding the observable relationship.
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
    assert history.json()["items"][1]["snapshot"]["observable_relationships"][0]["related_observable"]["uuid"] == str(
        obs1.uuid
    )
