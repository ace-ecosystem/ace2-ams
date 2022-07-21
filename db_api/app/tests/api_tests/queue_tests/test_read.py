import uuid

from fastapi import status

from tests import factory


#
# INVALID TESTS
#


def test_get_invalid_uuid(client):
    get = client.get("/api/queue/1")
    assert get.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_nonexistent_uuid(client):
    get = client.get(f"/api/queue/{uuid.uuid4()}")
    assert get.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_get_all(client, db):
    # Create some objects
    factory.queue.create_or_read(value="test", db=db)
    factory.queue.create_or_read(value="test2", db=db)

    # Read them back
    get = client.get("/api/queue/")
    assert get.status_code == status.HTTP_200_OK
    assert get.json()["total"] == 3  # The default analyst user has a queue
