from urllib.parse import unquote_plus, urlencode


def test_get_all_node_directives(client_valid_access_token, requests_mock):
    params = urlencode({"limit": 50, "offset": 0})

    requests_mock.get(
        f"http://db-api/api/node/directive/?{params}", json={"items": [], "total": 0, "limit": 50, "offset": 0}
    )

    client_valid_access_token.get(f"/api/node/directive/?{params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert unquote_plus(requests_mock.request_history[1].url) == unquote_plus(
        f"http://db-api/api/node/directive/?{params}"
    )
