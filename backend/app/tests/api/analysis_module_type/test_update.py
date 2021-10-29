import json
import pytest
import uuid

from fastapi import status


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", 123),
        ("description", ""),
        ("extended_version", 123),
        ("extended_version", ""),
        ("extended_version", []),
        ("manual", 123),
        ("manual", None),
        ("manual", "True"),
        ("observable_types", 123),
        ("observable_types", None),
        ("observable_types", "test_type"),
        ("observable_types", [123]),
        ("observable_types", [None]),
        ("observable_types", [""]),
        ("observable_types", ["abc", 123]),
        ("required_directives", 123),
        ("required_directives", None),
        ("required_directives", "test_type"),
        ("required_directives", [123]),
        ("required_directives", [None]),
        ("required_directives", [""]),
        ("required_directives", ["abc", 123]),
        ("required_tags", 123),
        ("required_tags", None),
        ("required_tags", "test_type"),
        ("required_tags", [123]),
        ("required_tags", [None]),
        ("required_tags", [""]),
        ("required_tags", ["abc", 123]),
        ("value", 123),
        ("value", None),
        ("value", ""),
        ("version", 123),
        ("version", None),
        ("version", ""),
        ("version", "v1.0"),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(f"/api/analysis/module_type/{uuid.uuid4()}", json={key: value})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/analysis/module_type/1", json={"value": "test_type"})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_duplicate_value_version(client_valid_access_token):
    # Create some objects
    client_valid_access_token.post("/api/analysis/module_type/", json={"value": "test", "version": "1.0.0"})
    create = client_valid_access_token.post("/api/analysis/module_type/", json={"value": "test", "version": "1.0.1"})

    # Ensure you cannot update an analysis module type to have a duplicate version+value combination
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"version": "1.0.0"})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(f"/api/analysis/module_type/{uuid.uuid4()}", json={"value": "test"})
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "api_endpoint,key,values",
    [
        ("/api/observable/type/", "observable_types", []),
        ("/api/observable/type/", "observable_types", ["test"]),
        ("/api/observable/type/", "observable_types", ["test1", "test2"]),
        ("/api/observable/type/", "observable_types", ["test", "test"]),
        ("/api/node/directive/", "required_directives", []),
        ("/api/node/directive/", "required_directives", ["test"]),
        ("/api/node/directive/", "required_directives", ["test1", "test2"]),
        ("/api/node/directive/", "required_directives", ["test", "test"]),
        ("/api/node/tag/", "required_tags", []),
        ("/api/node/tag/", "required_tags", ["test"]),
        ("/api/node/tag/", "required_tags", ["test1", "test2"]),
        ("/api/node/tag/", "required_tags", ["test", "test"]),
    ],
)
def test_update_valid_list_fields(client_valid_access_token, api_endpoint, key, values):
    # Create the analysis module type
    create = client_valid_access_token.post("/api/analysis/module_type/", json={"value": "test", "version": "1.0.0"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()[key]) == 0

    # Create the objects. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post(api_endpoint, json={"value": value})

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: values})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()[key]) == len(list(set(values)))


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("description", None, "test"),
        ("description", "test", "test"),
        ("extended_version", None, '{"foo": "bar"}'),
        ("extended_version", '{"foo": "bar"}', '{"foo": "bar"}'),
        ("manual", True, False),
        ("manual", False, False),
        ("value", "test", "test2"),
        ("value", "test", "test"),
        ("version", "1.0.0", "1.0.1"),
        ("version", "1.0.0", "1.0.0"),
    ],
)
def test_update(client_valid_access_token, key, initial_value, updated_value):
    # Create the object
    create_json = {"value": "test", "version": "1.0.0"}
    create_json[key] = initial_value
    create = client_valid_access_token.post("/api/analysis/module_type/", json=create_json)
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for extended_version, make sure the JSON form of the supplied string matches
    if key == "extended_version" and initial_value:
        assert get.json()[key] == json.loads(initial_value)
    else:
        assert get.json()[key] == initial_value

    # Update it
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: updated_value})
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for extended_version, make sure the JSON form of the supplied string matches
    if key == "extended_version":
        assert get.json()[key] == json.loads(updated_value)
    else:
        assert get.json()[key] == updated_value
