from uuid import uuid4


def test_get_observable(client_valid_access_token, requests_mock):
    observable_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/observable/{observable_uuid}",
        json={
            "type": {"uuid": str(uuid4()), "value": "test_type"},
            "value": "value",
            "node_type": "observable",
            "uuid": str(uuid4()),
            "directives": [],
            "observable_relationships": [],
            "permanent_tags": [],
            "threat_actors": [],
            "threats": [],
        },
    )

    client_valid_access_token.get(f"/api/observable/{observable_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/observable/{observable_uuid}"
