from uuid import uuid4


def test_update_alert(client_valid_access_token, requests_mock):
    alert_uuid = str(uuid4())

    requests_mock.patch("http://db-api/api/alert/?history_username=analyst", json=[{"uuid": alert_uuid}])

    client_valid_access_token.patch("/api/alert/", json=[{"uuid": alert_uuid}])

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "PATCH"
    assert requests_mock.request_history[1].url == "http://db-api/api/alert/?history_username=analyst"
