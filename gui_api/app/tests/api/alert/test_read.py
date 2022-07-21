import pytest

from datetime import datetime
from urllib.parse import unquote_plus, urlencode
from uuid import uuid4


@pytest.mark.parametrize(
    "param,value",
    [
        ("disposition", "FALSE_POSITIVE"),
        ("disposition_user", "analyst"),
        ("dispositioned_after", datetime.now()),
        ("dispositioned_before", datetime.now()),
        ("event_uuid", uuid4()),
        ("event_time_after", datetime.now()),
        ("event_time_before", datetime.now()),
        ("insert_time_after", datetime.now()),
        ("insert_time_before", datetime.now()),
        ("name", "test"),
        ("not_disposition", "test"),
        ("not_disposition_user", "test"),
        ("not_event_uuid", uuid4()),
        ("not_name", "test"),
        ("not_observable", "fqdn|test.com"),
        ("not_observable_types", "test"),
        ("not_observable_value", "test"),
        ("not_owner", "test"),
        ("not_queue", "test"),
        ("not_tags", "test"),
        ("not_tool", "test"),
        ("not_tool_instance", "test"),
        ("observable", "fqdn|test.com"),
        ("observable_types", "fqdn,ipv4"),
        ("observable_value", "test.com"),
        ("owner", "analyst"),
        ("queue", "test_queue"),
        ("sort", "disposition|desc"),
        ("tags", "tag1,tag2"),
        ("threat_actors", "actor1,actor2"),
        ("threats", "threat1,threat2"),
        ("tool", "test_tool"),
        ("tool_instance", "test_tool_instance"),
    ],
)
def test_get_all_alerts(client_valid_access_token, requests_mock, param, value):
    params = urlencode({"limit": 50, "offset": 0, "alert": True, param: value})

    requests_mock.get(
        f"http://db-api/api/submission/?{params}", json={"items": [], "total": 0, "limit": 50, "offset": 0}
    )

    client_valid_access_token.get(f"/api/alert/?{params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert unquote_plus(requests_mock.request_history[1].url) == unquote_plus(f"http://db-api/api/submission/?{params}")


# NOTE: This separate test is needed because the GUI API parameter uses "alert_type" but the
# DB API parameter uses "submission_type".
def test_get_all_alerts_alert_type(client_valid_access_token, requests_mock):
    gui_params = urlencode({"limit": 50, "offset": 0, "alert": True, "alert_type": "test_type"})
    db_params = urlencode({"limit": 50, "offset": 0, "alert": True, "submission_type": "test_type"})

    requests_mock.get(
        f"http://db-api/api/submission/?{db_params}", json={"items": [], "total": 0, "limit": 50, "offset": 0}
    )

    client_valid_access_token.get(f"/api/alert/?{gui_params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert unquote_plus(requests_mock.request_history[1].url) == unquote_plus(
        f"http://db-api/api/submission/?{db_params}"
    )


# NOTE: This separate test is needed because the GUI API parameter uses "not_alert_type" but the
# DB API parameter uses "not_submission_type".
def test_get_all_alerts_not_alert_type(client_valid_access_token, requests_mock):
    gui_params = urlencode({"limit": 50, "offset": 0, "alert": True, "not_alert_type": "test_type"})
    db_params = urlencode({"limit": 50, "offset": 0, "alert": True, "not_submission_type": "test_type"})

    requests_mock.get(
        f"http://db-api/api/submission/?{db_params}", json={"items": [], "total": 0, "limit": 50, "offset": 0}
    )

    client_valid_access_token.get(f"/api/alert/?{gui_params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert unquote_plus(requests_mock.request_history[1].url) == unquote_plus(
        f"http://db-api/api/submission/?{db_params}"
    )


def test_get_alert(client_valid_access_token, requests_mock):
    alert_uuid = uuid4()
    requests_mock.get(f"http://db-api/api/submission/{alert_uuid}", json={})

    client_valid_access_token.get(f"/api/alert/{alert_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/submission/{alert_uuid}"


def test_get_alert_history(client_valid_access_token, requests_mock):
    alert_uuid = uuid4()
    params = urlencode({"limit": 50, "offset": 0})
    requests_mock.get(
        f"http://db-api/api/submission/{alert_uuid}/history?{params}",
        json={"items": [], "total": 0, "limit": 50, "offset": 0},
    )

    client_valid_access_token.get(f"/api/alert/{alert_uuid}/history?{params}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/submission/{alert_uuid}/history?{params}"


def test_get_alerts_observables(client_valid_access_token, requests_mock):
    alert_uuid = str(uuid4())
    requests_mock.post(
        "http://db-api/api/submission/observables",
        json=[
            {
                "type": {"uuid": str(uuid4()), "value": "test_type"},
                "value": "value",
                "object_type": "observable",
                "uuid": str(uuid4()),
                "analysis_metadata": {"display_type": None, "display_value": None, "tags": []},
                "directives": [],
                "observable_relationships": [],
                "tags": [],
                "threat_actors": [],
                "threats": [],
            }
        ],
    )

    client_valid_access_token.post("/api/alert/observables", json=[alert_uuid])

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "POST"
    assert requests_mock.request_history[1].url == "http://db-api/api/submission/observables"


def test_get_url_domain_summary(client_valid_access_token, requests_mock):
    alert_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/submission/{alert_uuid}/summary/url_domain",
        json={"domains": [], "total": 0},
    )

    client_valid_access_token.get(f"/api/alert/{alert_uuid}/summary/url_domain")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/submission/{alert_uuid}/summary/url_domain"
