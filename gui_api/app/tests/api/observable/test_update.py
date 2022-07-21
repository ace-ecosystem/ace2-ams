from uuid import uuid4


def test_update_observable(client_valid_access_token, requests_mock):
    observable_uuid = str(uuid4())

    requests_mock.patch(f"http://db-api/api/observable/{observable_uuid}", json={"uuid": observable_uuid})

    client_valid_access_token.patch(f"/api/observable/{observable_uuid}", json={"uuid": observable_uuid})

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "PATCH"
    assert requests_mock.request_history[1].url == f"http://db-api/api/observable/{observable_uuid}"
