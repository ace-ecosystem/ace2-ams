import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_node_tree_nodes_invalid_uuid(client):
    get = client.post("/api/node/tree/observable", json=["1"])
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_node_tree_nodes_nonexistent_type(client, db):
    alert_tree = helpers.create_alert(db=db)

    get = client.post("/api/node/tree/abc", json=[str(alert_tree.node_uuid)])
    assert get.status_code == status.HTTP_404_NOT_FOUND


def test_get_node_tree_nodes_nonexistent_uuid(client):
    get = client.post("/api/node/tree/observable", json=[str(uuid.uuid4())])
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_node_tree_nodes(client, db):
    # Create an alert tree where the same observable type+value appears twice
    alert_tree = helpers.create_alert(db=db)
    observable1_tree = helpers.create_observable(type="fqdn", value="bad.com", parent_tree=alert_tree, db=db)
    helpers.create_observable(type="ipv4", value="127.0.0.1", parent_tree=alert_tree, db=db)
    analysis_tree = helpers.create_analysis(
        parent_tree=observable1_tree, parent_observable=observable1_tree.node, db=db
    )
    helpers.create_observable(type="fqdn", value="bad.com", parent_tree=analysis_tree, db=db)

    # Create a second alert tree with a duplicate observable from the first alert
    alert_tree2 = helpers.create_alert(db=db)
    helpers.create_observable(type="ipv4", value="127.0.0.1", parent_tree=alert_tree2, db=db)
    helpers.create_observable(type="email_address", value="badguy@bad.com", parent_tree=alert_tree2, db=db)

    # Fetching the list of observables in the NodeTrees should only show three observables since
    # there were duplicates:
    #
    # email_address: badguy@bad.com
    # fqdn: bad.com
    # ipv4: 127.0.0.1
    get = client.post("/api/node/tree/observable", json=[str(alert_tree.node_uuid), str(alert_tree2.node_uuid)])
    assert get.status_code == status.HTTP_200_OK
    assert len(get.json()) == 3
    assert any(o["type"]["value"] == "email_address" and o["value"] == "badguy@bad.com" for o in get.json())
    assert any(o["type"]["value"] == "fqdn" and o["value"] == "bad.com" for o in get.json())
    assert any(o["type"]["value"] == "ipv4" and o["value"] == "127.0.0.1" for o in get.json())
