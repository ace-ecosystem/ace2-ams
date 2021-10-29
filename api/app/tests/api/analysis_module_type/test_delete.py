import uuid

from fastapi import status


"""
NOTE: There are no tests for the foreign key constraints. The DELETE endpoint will need to be updated once the endpoints
are in place in order to account for this.
"""


#
# INVALID TESTS
#


def test_delete_invalid_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete("/api/analysis/module_type/1")
    assert delete.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_nonexistent_uuid(client_valid_access_token):
    delete = client_valid_access_token.delete(f"/api/analysis/module_type/{uuid.uuid4()}")
    assert delete.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_delete(client_valid_access_token):
    # Create a node directive
    directive_create = client_valid_access_token.post("/api/node/directive/", json={"value": "test_directive"})

    # Create a node tag
    tag_create = client_valid_access_token.post("/api/node/tag/", json={"value": "test_tag"})

    # Create an observable type
    type_create = client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create the analysis module type
    create = client_valid_access_token.post(
        "/api/analysis/module_type/",
        json={
            "observable_types": ["test_type"],
            "required_directives": ["test_directive"],
            "required_tags": ["test_tag"],
            "value": "initial",
            "version": "1.0.0",
        },
    )
    assert create.status_code == status.HTTP_201_CREATED

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK

    # Delete it
    delete = client_valid_access_token.delete(create.headers["Content-Location"])
    assert delete.status_code == status.HTTP_204_NO_CONTENT

    # Make sure it is gone
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.status_code == status.HTTP_404_NOT_FOUND

    # Make sure the node directive is still there
    get = client_valid_access_token.get(directive_create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_directive"

    # Make sure the node tag is still there
    get = client_valid_access_token.get(tag_create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_tag"

    # Make sure the observable type is still there
    get = client_valid_access_token.get(type_create.headers["Content-Location"])
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["value"] == "test_type"
