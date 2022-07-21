from uuid import uuid4


def test_create_observable(client_valid_access_token, requests_mock):
    requests_mock.post(
        "http://db-api/api/observable/",
        json=[{
            "uuid": "uuid1",
        }]
    )

    client_valid_access_token.post("/api/observable/", json=[{"type": "type", "value": "value"}])

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == f"http://db-api/api/observable/"
