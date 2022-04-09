from uuid import uuid4


def test_get_node_tree_nodes(client_valid_access_token, requests_mock):
    requests_mock.post("http://db-api/api/node/tree/observable", json=[])

    client_valid_access_token.post("/api/node/tree/observable", json=[str(uuid4())])

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/node/tree/observable"
