import os

from fastapi import status

#
# INVALID TESTS
#


def test_not_testing_mode_add_alerts(client):
    # Attempt to call the endpoint without being in testing mode
    os.environ["TESTING"] = "no"

    result = client.post("/api/test/add_alerts", json={"template": "blah.json", "count": 1})
    assert result.status_code == status.HTTP_403_FORBIDDEN
    assert result.json()["detail"] == "Unable to add test alerts when not running in TESTING mode"

    # Reset testing mode so future tests work
    os.environ["TESTING"] = "yes"


def test_not_testing_mode_add_event(client):
    # Attempt to call the endpoint without being in testing mode
    os.environ["TESTING"] = "no"

    result = client.post(
        "/api/test/add_event", json={"alert_template": "blah.json", "alert_count": 1, "name": "Test Event"}
    )
    assert result.status_code == status.HTTP_403_FORBIDDEN
    assert result.json()["detail"] == "Unable to add test event when not running in TESTING mode"

    # Reset testing mode so future tests work
    os.environ["TESTING"] = "yes"


def test_not_testing_mode_reset_database(client):
    # Attempt to call the endpoint without being in testing mode
    os.environ["TESTING"] = "no"

    result = client.post("/api/test/reset_database")
    assert result.status_code == status.HTTP_403_FORBIDDEN
    assert result.json()["detail"] == "Unable to reset the test database when not running in TESTING mode"

    # Reset testing mode so future tests work
    os.environ["TESTING"] = "yes"


#
# VALID TESTS
#


def test_add_alerts(client):
    get = client.get("/api/submission/")
    assert get.json()["total"] == 0

    result = client.post("/api/test/add_alerts", json={"template": "small.json", "count": 1})
    assert result.status_code == status.HTTP_204_NO_CONTENT

    get = client.get("/api/submission/")
    assert get.json()["total"] == 1


def test_add_event(client):
    get = client.get("/api/submission/")
    assert get.json()["total"] == 0
    get = client.get("/api/event/")
    assert get.json()["total"] == 0

    result = client.post(
        "/api/test/add_event", json={"alert_template": "small.json", "alert_count": 1, "name": "Test Event", "status": "OPEN"}
    )
    assert result.status_code == status.HTTP_204_NO_CONTENT

    get = client.get("/api/submission/")
    assert get.json()["total"] == 1
    get = client.get("/api/event/")
    assert get.json()["total"] == 1
