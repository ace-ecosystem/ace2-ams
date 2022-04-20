import uuid

from fastapi import status

from tests import helpers


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client):
    delete = client.delete("/api/node/relationship/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client):
    delete = client.delete(f"/api/node/relationship/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client, db):
    # Create some nodes
    alert_tree1 = helpers.create_alert(db=db)
    alert_tree2 = helpers.create_alert(db=db)

    # Create the object
    obj = helpers.create_node_relationship(node=alert_tree1.node, related_node=alert_tree2.node, type="test_rel", db=db)

    # Read it back
    get = client.get(f"/api/node/relationship/{obj.uuid}")
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client.delete(f"/api/node/relationship/{obj.uuid}")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client.get(f"/api/node/relationship/{obj.uuid}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_delete_verify_observable(client, db):
    # Create some nodes with relationships
    #
    # alert
    #   o
    #     analysis
    #       o1
    #       o2 - IS_HASH_OF o1
    alert_tree = helpers.create_alert(db=db, history_username="analyst")
    observable_tree = helpers.create_observable(type="ipv4", value="127.0.0.1", parent_tree=alert_tree, db=db)
    analysis_tree = helpers.create_analysis(db=db, parent_tree=observable_tree, parent_observable=observable_tree.node)
    observable_tree1 = helpers.create_observable(
        type="test_type", value="test_value", parent_tree=analysis_tree, db=db, history_username="analyst"
    )
    observable_tree2 = helpers.create_observable(
        type="test_type", value="test_value2", parent_tree=analysis_tree, db=db, history_username="analyst"
    )
    initial_version = observable_tree2.node.version
    relationship = helpers.create_node_relationship(
        node=observable_tree2.node, related_node=observable_tree1.node, type="IS_HASH_OF", db=db
    )

    # Delete the relationship
    delete = client.delete(f"/api/node/relationship/{relationship.uuid}?history_username=analyst")
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Removing a relationship counts as modifying the node, so it should have a new version
    assert observable_tree2.node.version != initial_version

    # Verify the observable history. The first record is for creating the observable, and
    # the second record is from removing the node relationship.
    history = client.get(f"/api/observable/{observable_tree2.node_uuid}/history")
    assert len(history.json()["items"]) == 2
    assert history.json()["items"][1]["action"] == "UPDATE"
    assert history.json()["items"][1]["action_by"]["username"] == "analyst"
    assert history.json()["items"][1]["record_uuid"] == str(observable_tree2.node_uuid)
    assert history.json()["items"][1]["field"] == "relationships"
    assert history.json()["items"][1]["diff"]["old_value"] is None
    assert history.json()["items"][1]["diff"]["new_value"] is None
    assert history.json()["items"][1]["diff"]["added_to_list"] == []
    assert history.json()["items"][1]["diff"]["removed_from_list"] == [str(observable_tree1.node_uuid)]
    assert history.json()["items"][1]["snapshot"]["observable_relationships"] == []
