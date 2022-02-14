import pytest
import uuid

from fastapi import status

from db.schemas.observable import Observable
from tests.api.node import INVALID_LIST_STRING_VALUES, VALID_LIST_STRING_VALUES
from tests import helpers


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", 123),
        ("context", ""),
        ("expires_on", ""),
        ("expires_on", "Monday"),
        ("expires_on", "2022-01-01"),
        ("for_detection", 123),
        ("for_detection", None),
        ("for_detection", "True"),
        ("redirection_uuid", 123),
        ("redirection_uuid", ""),
        ("redirection_uuid", "abc"),
        ("time", None),
        ("time", ""),
        ("time", "Monday"),
        ("time", "2022-01-01"),
        ("type", 123),
        ("type", None),
        ("type", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("uuid", ""),
        ("value", 123),
        ("value", None),
        ("value", ""),
    ],
)
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {
        "node_tree": {"root_node_uuid": str(uuid.uuid4())},
        "type": "test_type",
        "value": "test",
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/observable/", json=[create_json])
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) == 1
    assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key,values",
    [
        ("directives", INVALID_LIST_STRING_VALUES),
        ("tags", INVALID_LIST_STRING_VALUES),
        ("threat_actors", INVALID_LIST_STRING_VALUES),
        ("threats", INVALID_LIST_STRING_VALUES),
    ],
)
def test_create_invalid_node_fields(client_valid_access_token, key, values):
    for value in values:
        create = client_valid_access_token.post(
            "/api/observable/",
            json=[
                {
                    key: value,
                    "node_tree": {"root_node_uuid": str(uuid.uuid4())},
                    "type": "test_type",
                    "value": "test",
                }
            ],
        )
        assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, db, key):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an object
    create1_json = {
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
        "type": "test_type",
        "uuid": str(uuid.uuid4()),
        "value": "test",
    }
    client_valid_access_token.post("/api/observable/", json=[create1_json])

    # Ensure you cannot create another object with the same unique field value
    create2_json = {
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
        "type": "test_type",
        "value": "test2",
    }
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/observable/", json=[create2_json])
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_duplicate_type_value(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an object
    client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": "test_type",
                "value": "test",
            }
        ],
    )

    # Ensure you cannot create another observable with the same type+value combination in the same node tree location
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": "test_type",
                "value": "test",
            }
        ],
    )

    assert create.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("type"),
        ("value"),
    ],
)
def test_create_missing_required_fields(client_valid_access_token, key):
    create_json = {"type": "test_type", "value": "test"}
    del create_json[key]
    create = client_valid_access_token.post("/api/observable/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_nonexistent_alert(client_valid_access_token, db):
    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    nonexistent_uuid = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[{"node_tree": {"root_node_uuid": nonexistent_uuid}, "type": "test_type", "value": "test"}],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_uuid in create.text


@pytest.mark.parametrize(
    "key",
    [("directives"), ("tags"), ("threat_actors"), ("threats")],
)
def test_create_nonexistent_node_fields(client_valid_access_token, db, key):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                key: ["abc"],
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": "test_type",
                "value": "test",
            }
        ],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert "abc" in create.text


def test_create_nonexistent_redirection(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    nonexistent_uuid = str(uuid.uuid4())
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "redirection_uuid": nonexistent_uuid,
                "type": "test_type",
                "value": "test",
            }
        ],
    )

    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_uuid in create.text


def test_create_nonexistent_type(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    nonexistent_type = "test_type"
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": nonexistent_type,
                "value": "test",
            }
        ],
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND
    assert nonexistent_type in create.text


#
# VALID TESTS
#


def test_create_verify_history(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create some observables
    observables = []
    for i in range(3):
        observables.append(
            {
                "uuid": str(uuid.uuid4()),
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": "test_type",
                "value": f"test{i}",
            }
        )
    create = client_valid_access_token.post("/api/observable/", json=observables)
    assert create.status_code == status.HTTP_201_CREATED

    # Verify the history records
    for observable in observables:
        history = client_valid_access_token.get(f"/api/observable/{observable['uuid']}/history")
        assert history.json()["total"] == 1
        assert history.json()["items"][0]["action"] == "CREATE"
        assert history.json()["items"][0]["action_by"]["username"] == "analyst"
        assert history.json()["items"][0]["record_uuid"] == observable["uuid"]
        assert history.json()["items"][0]["field"] is None
        assert history.json()["items"][0]["diff"] is None
        assert history.json()["items"][0]["snapshot"]["value"] == observable["value"]


def test_create_bulk(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)
    initial_alert_version = node_tree.root_node.version

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create some observables
    observables = []
    for i in range(3):
        observables.append(
            {
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": "test_type",
                "value": f"test{i}",
            }
        )
    create = client_valid_access_token.post("/api/observable/", json=observables)
    assert create.status_code == status.HTTP_201_CREATED

    # There should be 3 observables in the database
    observables = db.query(Observable).all()
    assert len(observables) == 3

    # Additionally, creating an observable should trigger the alert to get a new version.
    assert node_tree.root_node.version != initial_alert_version


def test_create_node_metadata(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                "node_tree": {
                    "node_metadata": {"display": {"type": "override_type", "value": "override_value"}},
                    "parent_tree_uuid": str(node_tree.uuid),
                    "root_node_uuid": str(node_tree.root_node_uuid),
                },
                "type": "test_type",
                "value": "test",
            }
        ],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read the alert back to get its tree structure that contains the observable to verify its node_metadata
    get = client_valid_access_token.get(f"http://testserver/api/alert/{node_tree.root_node_uuid}")
    assert get.json()["children"][0]["node_metadata"] == {
        "display": {"type": "override_type", "value": "override_value"}
    }


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", None),
        ("context", "test"),
        ("expires_on", None),
        ("expires_on", 1640995200),
        ("expires_on", "2022-01-01T00:00:00Z"),
        ("expires_on", "2022-01-01 00:00:00"),
        ("expires_on", "2022-01-01 00:00:00.000000"),
        ("expires_on", "2021-12-31 19:00:00-05:00"),
        ("for_detection", False),
        ("for_detection", True),
        ("time", 1640995200),
        ("time", "2022-01-01T00:00:00Z"),
        ("time", "2022-01-01 00:00:00"),
        ("time", "2022-01-01 00:00:00.000000"),
        ("time", "2021-12-31 19:00:00-05:00"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client_valid_access_token, db, key, value):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                key: value,
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": "test_type",
                "value": "test",
            }
        ],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for expires_on, make sure that the retrieved value matches the proper UTC timestamp
    if (key == "expires_on" or key == "time") and value:
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == value


def test_create_valid_redirection(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create an observable
    observable_uuid = str(uuid.uuid4())
    create_json = {
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
        "type": "test_type",
        "uuid": observable_uuid,
        "value": "test",
    }
    client_valid_access_token.post("/api/observable/", json=[create_json])

    # Create another observable that redirects to the previously created one
    create_json = {
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
        "redirection_uuid": observable_uuid,
        "type": "test_type",
        "value": "test2",
    }
    create = client_valid_access_token.post("/api/observable/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["redirection_uuid"] == observable_uuid


def test_create_valid_required_fields(client_valid_access_token, db):
    # Create an alert
    node_tree = helpers.create_alert(db=db)

    # Create an observable type
    helpers.create_observable_type(value="test_type", db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/observable/",
        json=[
            {
                "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
                "type": "test_type",
                "value": "test",
            }
        ],
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"


@pytest.mark.parametrize(
    "key,value_lists,helper_create_func",
    [
        ("directives", VALID_LIST_STRING_VALUES, helpers.create_node_directive),
        ("tags", VALID_LIST_STRING_VALUES, helpers.create_node_tag),
        ("threat_actors", VALID_LIST_STRING_VALUES, helpers.create_node_threat_actor),
        ("threats", VALID_LIST_STRING_VALUES, helpers.create_node_threat),
    ],
)
def test_create_valid_node_fields(client_valid_access_token, db, key, value_lists, helper_create_func):
    for value_list in value_lists:
        for value in value_list:
            helper_create_func(value=value, db=db)

        # Create an alert
        node_tree = helpers.create_alert(db=db)

        # Create an observable type
        helpers.create_observable_type(value="test_type", db=db)

        create = client_valid_access_token.post(
            "/api/observable/",
            json=[
                {
                    key: value_list,
                    "node_tree": {
                        "parent_tree_uuid": str(node_tree.uuid),
                        "root_node_uuid": str(node_tree.root_node_uuid),
                    },
                    "type": "test_type",
                    "value": f"{key}{value_list}",
                }
            ],
        )
        assert create.status_code == status.HTTP_201_CREATED

        # Read it back
        get = client_valid_access_token.get(create.headers["Content-Location"])
        assert len(get.json()[key]) == len(list(set(value_list)))
