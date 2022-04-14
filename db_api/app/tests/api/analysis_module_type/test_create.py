import json
import pytest
import uuid

from fastapi import status

from tests import helpers


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
        ("uuid", 123),
        ("uuid", None),
        ("uuid", ""),
        ("uuid", "abc"),
        ("value", 123),
        ("value", None),
        ("value", ""),
        ("version", 123),
        ("version", None),
        ("version", ""),
        ("version", "v1.0"),
    ],
)
def test_create_invalid_fields(client, key, value):
    create_json = {"value": "test"}
    create_json[key] = value
    create = client.post("/api/analysis/module_type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("uuid"),
    ],
)
def test_create_duplicate_unique_fields(client, key):
    # Create an object
    create1_json = {"uuid": str(uuid.uuid4()), "value": "test", "version": "1.0.0"}
    client.post("/api/analysis/module_type/", json=create1_json)

    # Ensure you cannot create another object with the same unique field value
    create2_json = {"value": "test2", "version": "1.0.0"}
    create2_json[key] = create1_json[key]
    create2 = client.post("/api/analysis/module_type/", json=create2_json)
    assert create2.status_code == status.HTTP_409_CONFLICT


def test_create_duplicate_version_value(client):
    # Create an object
    client.post("/api/analysis/module_type/", json={"value": "test", "version": "1.0.0"})

    # Ensure you cannot create another object with the same unique value+version combination
    create = client.post("/api/analysis/module_type/", json={"value": "test", "version": "1.0.0"})
    assert create.status_code == status.HTTP_409_CONFLICT


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
        ("version"),
    ],
)
def test_create_missing_required_fields(client, key):
    create_json = {"value": "test", "version": "1.0.0"}
    del create_json[key]
    create = client.post("/api/analysis/module_type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("observable_types"),
        ("required_directives"),
        ("required_tags"),
    ],
)
def test_create_nonexistent_list_values(client, key):
    create = client.post(
        "/api/analysis/module_type/", json={"value": "test", "version": "1.0.0", key: ["test_value"]}
    )
    assert create.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("description", None),
        ("description", "test"),
        ("extended_version", None),
        ("extended_version", '{"foo": "bar"}'),
        ("manual", True),
        ("manual", False),
        ("uuid", str(uuid.uuid4())),
    ],
)
def test_create_valid_optional_fields(client, key, value):
    # Create the object
    create = client.post(
        "/api/analysis/module_type/", json={key: value, "value": "test", "version": "1.0.0"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])

    # If the test is for extended_version, make sure the JSON form of the supplied string matches
    if key == "extended_version" and value:
        assert get.json()[key] == json.loads(value)
    else:
        assert get.json()[key] == value


@pytest.mark.parametrize(
    "key,values",
    [
        ("observable_types", []),
        ("observable_types", ["test"]),
        ("observable_types", ["test1", "test2"]),
        ("observable_types", ["test", "test"]),
        ("required_directives", []),
        ("required_directives", ["test"]),
        ("required_directives", ["test1", "test2"]),
        ("required_directives", ["test", "test"]),
        ("required_tags", []),
        ("required_tags", ["test"]),
        ("required_tags", ["test1", "test2"]),
        ("required_tags", ["test", "test"]),
    ],
)
def test_create_valid_list_fields(client, db, key, values):
    # Create the objects
    if key == "observable_types":
        create_func = helpers.create_observable_type
    elif key == "required_directives":
        create_func = helpers.create_node_directive
    else:
        create_func = helpers.create_node_tag

    for value in values:
        create_func(value=value, db=db)

    # Create the analysis module type
    create = client.post(
        "/api/analysis/module_type/", json={key: values, "value": "test", "version": "1.0.0"}
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()[key]) == len(list(set(values)))


def test_create_valid_required_fields(client):
    # Create the object
    create = client.post("/api/analysis/module_type/", json={"value": "test", "version": "1.0.0"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["value"] == "test"
