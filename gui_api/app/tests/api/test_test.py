from fastapi import status


def test_add_alerts(client_valid_access_token, requests_mock):
    requests_mock.post("http://db-api/api/test/add_alerts", status_code=status.HTTP_204_NO_CONTENT)

    client_valid_access_token.post("/api/test/add_alerts", json={"template": "test.json", "count": 1})

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/test/add_alerts"


def test_add_event(client_valid_access_token, requests_mock):
    requests_mock.post("http://db-api/api/test/add_event", status_code=status.HTTP_204_NO_CONTENT)

    client_valid_access_token.post(
        "/api/test/add_event", json={"alert_template": "test.json", "alert_count": 1, "name": "Test Event"}
    )

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/test/add_event"
