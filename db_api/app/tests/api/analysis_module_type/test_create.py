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
        ("cache_seconds", None),
        ("cache_seconds", ""),
        ("cache_seconds", "abc"),
        ("cache_seconds", "1"),
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
    create_json = {"cache_seconds": 90, "value": "test", key: value}
    create = client.post("/api/analysis/module_type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize(
    "key",
    [
        ("value"),
    ],
)
def test_create_missing_required_fields(client, key):
    create_json = {"value": "test"}
    del create_json[key]
    create = client.post("/api/analysis/module_type/", json=create_json)
    assert create.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


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
        "/api/analysis/module_type/",
        json={key: value, "cache_seconds": 90, "value": "test", "version": "1.0.0"},
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
    # Create the analysis module type
    create = client.post(
        "/api/analysis/module_type/",
        json={key: values, "cache_seconds": 90, "value": "test", "version": "1.0.0"},
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert len(get.json()[key]) == len(list(set(values)))


def test_create_valid_required_fields(client):
    # Create the object
    create = client.post("/api/analysis/module_type/", json={"cache_seconds": 90, "value": "test", "version": "1.0.0"})
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client.get(create.headers["Content-Location"])
    assert get.json()["cache_seconds"] == 90.0
    assert get.json()["value"] == "test"
