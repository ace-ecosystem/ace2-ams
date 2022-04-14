import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/observable/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/observable/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get(client, db):
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test_value", parent_tree=alert_tree, db=db)

    get = client.get(f"/api/observable/{observable_tree.node.uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["node_type"] == "observable"


def test_get_all(client, db):
    alert_tree = helpers.create_alert(db=db)
    observable_tree = helpers.create_observable(type="test_type", value="test", parent_tree=alert_tree, db=db)
    helpers.create_observable(type="test_type", value="test2", parent_tree=alert_tree, db=db)

    # Adding a third observable somewhere in the alert tree with the same type+value combination is allowed,
    # but it will not result in a third entry in the observable table.
    helpers.create_observable(type="test_type", value="test2", parent_tree=observable_tree, db=db)

    # Read them back
    get = client.get("/api/observable/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 2


def test_get_all_empty(client):
    get = client.get("/api/observable/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 0


def test_observable_relationships(client, db):
    # Create some nodes with relationships
    #
    # alert
    #   analysis
    #     o1
    #     o2
    #     o3 - IS_HASH_OF o1, IS_EQUAL_TO o2, BLAH analysis
    alert_tree = helpers.create_alert(db=db)
    analysis_tree = helpers.create_analysis(db=db, parent_tree=alert_tree)
    observable_tree1 = helpers.create_observable(type="test_type", value="test_value", parent_tree=analysis_tree, db=db)
    observable_tree2 = helpers.create_observable(
        type="test_type", value="test_value2", parent_tree=analysis_tree, db=db
    )
    observable_tree3 = helpers.create_observable(
        type="test_type", value="test_value3", parent_tree=analysis_tree, db=db
    )
    helpers.create_node_relationship(
        node=observable_tree3.node, related_node=observable_tree1.node, type="IS_HASH_OF", db=db
    )
    helpers.create_node_relationship(
        node=observable_tree3.node, related_node=observable_tree2.node, type="IS_EQUAL_TO", db=db
    )
    helpers.create_node_relationship(node=observable_tree3.node, related_node=analysis_tree.node, type="BLAH", db=db)

    # The o2 observable has three relationships but only two observable relationship. The observable relationships
    # should be sorted by the related observable's type then value.
    get = client.get(f"/api/observable/{observable_tree3.node_uuid}")
    assert get.status_code == status.HTTP_200_OK
    assert len(observable_tree3.node.relationships) == 3
    assert len(get.json()["observable_relationships"]) == 2
    assert get.json()["observable_relationships"][0]["type"]["value"] == "IS_HASH_OF"
    assert get.json()["observable_relationships"][0]["related_node"]["uuid"] == str(observable_tree1.node_uuid)
    assert get.json()["observable_relationships"][1]["type"]["value"] == "IS_EQUAL_TO"
    assert get.json()["observable_relationships"][1]["related_node"]["uuid"] == str(observable_tree2.node_uuid)
