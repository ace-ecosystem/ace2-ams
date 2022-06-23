import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/observable/relationship/1?history_username=analyst")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/observable/relationship/{uuid.uuid4()}?history_username=analyst")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    # Create some observables
    alert = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(type="type1", value="value1", parent_analysis=alert.root_analysis, db=db)
    obs2 = factory.observable.create_or_read(type="type2", value="value2", parent_analysis=alert.root_analysis, db=db)

    # Create the object
    obj = factory.observable_relationship.create_or_read(
        observable=obs1, related_observable=obs2, type="test_rel", db=db
    )

    # Read it back
    get = client.get(f"/api/observable/relationship/{obj.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client.delete(f"/api/observable/relationship/{obj.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/observable/relationship/{obj.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_verify_observable(client, db):
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
    relationship = factory.observable_relationship.create_or_read(
        observable=obs2, related_observable=obs1, type="IS_HASH_OF", db=db
    )

    # Delete the relationship
    delete = client.delete(f"/api/observable/relationship/{relationship.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Removing a relationship counts as modifying the observable, so it should have a new version
    assert obs2.version != initial_version

    # Verify the observable history. The first record is for creating the observable, and
    # the second record is from removing the observable relationship.
    history = client.get(f"/api/observable/{obs2.uuid}/history")
    assert len(history.json()["items"]) == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(obs2.uuid)
    assert history.json()["items"][1]["field"] == "relationships"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == []
    assert history.json()["items"][1]["diff"]["removed_from_list"] == [str(obs1.uuid)]
    assert history.json()["items"][1]["snapshot"]["observable_relationships"] == []
