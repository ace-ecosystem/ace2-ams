def test_create_event(client_valid_access_token, requests_mock):
    requests_mock.post("http://db-api/api/event/", json={"uuid": "uuid1"})

    client_valid_access_token.post(
        "/api/event/",
        json={
            "name": "test event",
            "queue": "test_queue",
            "status": "OPEN",
        },
    )

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/event/"
