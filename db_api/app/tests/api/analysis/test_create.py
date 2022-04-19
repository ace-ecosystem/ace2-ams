import json
import pytest
import time
import uuid

from datetime import datetime
from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("analysis_module_type", 123),
        ("analysis_module_type", ""),
        ("analysis_module_type", "abc"),
        ("details", 123),
        ("details", ""),
        ("details", "abc"),
        ("details", []),
        ("error_message", 123),
        ("error_message", ""),
        ("stack_trace", 123),
        ("stack_trace", ""),
        ("summary", 123),
        ("summary", ""),
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {
        "node_tree": {"root_node_uuid": str(uuid.uuid4())},
    }
    create_json[key] = value
    create = client.post("/api/analysis/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) == 1
    assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client, db, key):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create an object
    create1_json = {
        "uuid": str(uuid.uuid4()),
        "analysis_module_type": str(analysis_module_type.uuid),
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
    }
    client.post("/api/analysis/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {
        "analysis_module_type": str(analysis_module_type.uuid),
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
    }
    create2_json[key] = create1_json[key]
    create2 = client.post("/api/analysis/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_analysis_module_type(client, db):
    node_tree = helpers.create_alert(db=db)

    create = client.post(
        "/api/analysis/",
        json={
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            "analysis_module_type": str(uuid.uuid4()),
        },
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_invalid_email_analysis(client, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="Email Analysis", db=db)

    # Create the analysis - it is missing the required "from_address" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            "details": json.dumps(
                {
                    "attachments": [],
                    "cc_addresses": [],
                    "headers": "blah",
                    "message_id": "<abcd1234@evil.com>",
                    "subject": "Hello",
                    "time": datetime.now().isoformat(),
                    "to_address": "goodguy@company.com",
                    "extra_field": "extra_value",
                }
            ),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


def test_create_invalid_faqueue_analysis(client, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="FA Queue Analysis", db=db)

    # Create the analysis - it is missing the required "hits" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            "details": json.dumps({"faqueue_hits": 100, "link": "https://example.com"}),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


def test_create_invalid_sandbox_analysis(client, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="Sandbox Analysis - Sandbox1", db=db)

    # Create the analysis - it is missing the required "filename" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            "details": json.dumps({"sandbox_url": "http://url.to.sandbox.report"}),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


def test_create_invalid_user_analysis(client, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="User Analysis", db=db)

    # Create the analysis - it is missing the required "user_id" key
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            "details": json.dumps({"username": "goodguy", "email": "goodguy@company.com"}),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


def test_create_node_metadata(client, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create the object
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {
                "node_metadata": {"display": {"type": "override_type", "value": "override_value"}},
                "parent_tree_uuid": str(node_tree.uuid),
                "root_node_uuid": str(node_tree.root_node_uuid),
            },
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read the alert back to get its tree structure that contains the analysis to verify its node_metadata
    get = client.get(f"http://testserver/api/alert/{node_tree.root_node_uuid}")
    assert get.json()["children"][0]["node_metadata"] == {
        "display": {"type": "override_type", "value": "override_value"}
    }


@pytest.mark.parametrize(
    "key,value",
    [
        ("details", None),
        ("details", "{}"),
        ("details", '{"foo": "bar"}'),
        ("error_message", None),
        ("error_message", "test"),
        ("stack_trace", None),
        ("stack_trace", "test"),
        ("summary", None),
        ("summary", "test"),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client, db, key, value):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create the object
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            key: value,
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details" and value:
        assert get.json()[key] == json.loads(value)
    else:
        assert get.json()[key] == value


def test_create_valid_required_fields(client, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create the object
    create = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back, but since there are no required fields to create the analysis, there is nothing to verify.
    get = client.get(create.headers["Content-Location"])
    assert get.status_code == 200


def test_cached_analysis(client, db):
    # Create the first alert and add the analysis to it.
    alert_tree1 = helpers.create_alert(db=db)
    observable_tree1 = helpers.create_observable(type="ipv4", value="127.0.0.1", parent_tree=alert_tree1, db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create the analysis
    create1 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "node_tree": {
                "parent_tree_uuid": str(observable_tree1.uuid),
                "root_node_uuid": str(alert_tree1.root_node_uuid),
            },
            "parent_observable_uuid": str(observable_tree1.node_uuid),
            "run_time": str(datetime.utcnow()),
        },
    )
    assert create1.status_code == status.HTTP_201_CREATED

    # Create a second alert with the same observable and analysis type. This should be cached.
    alert_tree2 = helpers.create_alert(db=db)
    observable_tree2 = helpers.create_observable(type="ipv4", value="127.0.0.1", parent_tree=alert_tree2, db=db)

    # Create the analysis
    create2 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "node_tree": {
                "parent_tree_uuid": str(observable_tree2.uuid),
                "root_node_uuid": str(alert_tree2.root_node_uuid),
            },
            "parent_observable_uuid": str(observable_tree2.node_uuid),
            "run_time": str(datetime.utcnow()),
        },
    )
    assert create2.status_code == status.HTTP_201_CREATED

    # The Content-Location headers should be the same from the two create API calls, which
    # indicates that the existing/cached analysis was used for the second API call.
    assert create1.headers["Content-Location"] == create2.headers["Content-Location"]


def test_expired_cached_analysis(client, db):
    # Create the first alert and add the analysis to it.
    alert_tree1 = helpers.create_alert(db=db)
    observable_tree1 = helpers.create_observable(type="ipv4", value="127.0.0.1", parent_tree=alert_tree1, db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", cache_seconds=1, db=db)

    # Create the analysis
    create1 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "node_tree": {
                "parent_tree_uuid": str(observable_tree1.uuid),
                "root_node_uuid": str(alert_tree1.root_node_uuid),
            },
            "parent_observable_uuid": str(observable_tree1.node_uuid),
            "run_time": str(datetime.utcnow()),
        },
    )
    assert create1.status_code == status.HTTP_201_CREATED

    # Sleep so that the analysis expires from the cache
    time.sleep(2)

    # Create a second alert with the same observable and analysis type. The cache is expired.
    alert_tree2 = helpers.create_alert(db=db)
    observable_tree2 = helpers.create_observable(type="ipv4", value="127.0.0.1", parent_tree=alert_tree2, db=db)

    # Create the analysis
    create2 = client.post(
        "/api/analysis/",
        json={
            "analysis_module_type_uuid": str(analysis_module_type.uuid),
            "node_tree": {
                "parent_tree_uuid": str(observable_tree2.uuid),
                "root_node_uuid": str(alert_tree2.root_node_uuid),
            },
            "parent_observable_uuid": str(observable_tree2.node_uuid),
            "run_time": str(datetime.utcnow()),
        },
    )
    assert create2.status_code == status.HTTP_201_CREATED

    # The Content-Location headers NOT should be the same from the two create API calls, which
    # indicates that the existing/cached analysis was expired and a new one was created.
    assert create1.headers["Content-Location"] != create2.headers["Content-Location"]
