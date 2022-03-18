import json
import pytest
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
def test_create_invalid_fields(client_valid_access_token, key, value):
    create_json = {
        "node_tree": {"root_node_uuid": str(uuid.uuid4())},
    }
    create_json[key] = value
    create = client_valid_access_token.post("/api/analysis/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(create.json()["detail"]) == 1
    assert key in create.json()["detail"][0]["loc"]


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client_valid_access_token, db, key):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create an object
    create1_json = {
        "uuid": str(uuid.uuid4()),
        "analysis_module_type": str(analysis_module_type.uuid),
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
    }
    client_valid_access_token.post("/api/analysis/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {
        "analysis_module_type": str(analysis_module_type.uuid),
        "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
    }
    create2_json[key] = create1_json[key]
    create2 = client_valid_access_token.post("/api/analysis/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_nonexistent_analysis_module_type(client_valid_access_token, db):
    node_tree = helpers.create_alert(db=db)

    create = client_valid_access_token.post(
        "/api/analysis/",
        json={
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            "analysis_module_type": str(uuid.uuid4()),
        },
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


def test_create_invalid_email_analysis(client_valid_access_token, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="Email Analysis", db=db)

    # Create the analysis - it is missing the required "from_address" key
    create = client_valid_access_token.post(
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


def test_create_invalid_faqueue_analysis(client_valid_access_token, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="FA Queue Analysis", db=db)

    # Create the analysis - it is missing the required "hits" key
    create = client_valid_access_token.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            "details": json.dumps({"faqueue_hits": 100, "link": "https://example.com"}),
        },
    )

    assert create.status_code == status.HTTP_400_BAD_REQUEST


#
# VALID TESTS
#


def test_create_node_metadata(client_valid_access_token, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create the object
    create = client_valid_access_token.post(
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
    get = client_valid_access_token.get(f"http://testserver/api/alert/{node_tree.root_node_uuid}")
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
def test_create_valid_optional_fields(client_valid_access_token, db, key, value):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
            key: value,
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for details, make sure the JSON form of the supplied string matches
    if key == "details" and value:
        assert get.json()[key] == json.loads(value)
    else:
        assert get.json()[key] == value


def test_create_valid_required_fields(client_valid_access_token, db):
    node_tree = helpers.create_alert(db=db)
    analysis_module_type = helpers.create_analysis_module_type(value="test", db=db)

    # Create the object
    create = client_valid_access_token.post(
        "/api/analysis/",
        json={
            "analysis_module_type": str(analysis_module_type.uuid),
            "node_tree": {"parent_tree_uuid": str(node_tree.uuid), "root_node_uuid": str(node_tree.root_node_uuid)},
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back, but since there are no required fields to create the analysis, there is nothing to verify.
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == 200
