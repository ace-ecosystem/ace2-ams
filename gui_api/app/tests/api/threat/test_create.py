from uuid import uuid4


def test_create_threat(client_valid_access_token, requests_mock):
    requests_mock.post("http://db-api/api/node/threat/", json={"uuid": "uuid1"})

    client_valid_access_token.post(
        "/api/node/threat/",
        json={"types": ["type1", "type2"], "value": "value", "queues": ["queue1"]},
    )

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/node/threat/"
