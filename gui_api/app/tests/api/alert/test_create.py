def test_create_alert(client_valid_access_token, requests_mock):
    requests_mock.post("http://db-api/api/alert/?history_username=analyst", json={"uuid": "uuid1"})

    client_valid_access_token.post(
        "/api/alert/",
        json={
            "name": "test alert",
            "queue": "test_queue",
            "observables": [{"type": "o_type", "value": "o_value"}],
            "type": "test_type",
        },
    )

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/alert/?history_username=analyst"
