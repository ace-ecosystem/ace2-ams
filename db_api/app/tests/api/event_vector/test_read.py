import uuid

from fastapi import status

from tests import helpers


#
# INVALID TESTS
#


def test_get_invalid_uuid(client_valid_access_token):
    get = client_valid_access_token.get("/api/event/vector/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client_valid_access_token):
    get = client_valid_access_token.get(f"/api/event/vector/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client_valid_access_token, db):
    # Create some objects
    helpers.create_event_vector(value="test", queues=["internal"], db=db)
    helpers.create_event_vector(value="test2", queues=["external"], db=db)
    helpers.create_event_vector(value="test3", queues=["internal", "external"], db=db)

    # Read them back
    get = client_valid_access_token.get("/api/event/vector/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 3

    # Sort them by their names so we know the order
    results = sorted(get.json()["items"], key=lambda x: x["value"])

    assert len(results[0]["queues"]) == 1
    assert results[0]["queues"][0]["value"] == "internal"

    assert len(results[1]["queues"]) == 1
    assert results[1]["queues"][0]["value"] == "external"

    assert len(results[2]["queues"]) == 2
    assert any(x["value"] == "internal" for x in results[2]["queues"])
    assert any(x["value"] == "external" for x in results[2]["queues"])


def test_get_all_empty(client_valid_access_token):
    get = client_valid_access_token.get("/api/event/vector/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 0
