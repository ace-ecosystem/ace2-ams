from datetime import datetime
from uuid import uuid4


def test_get_node_detection_point(client_valid_access_token, requests_mock):
    node_detection_point_uuid = uuid4()
    requests_mock.get(
        f"http://db-api/api/node/detection_point/{node_detection_point_uuid}",
        json={"node_uuid": str(uuid4()), "value": "value", "insert_time": str(datetime.now()), "uuid": str(uuid4())},
    )

    client_valid_access_token.get(f"/api/node/detection_point/{node_detection_point_uuid}")

    assert (len(requests_mock.request_history)) == 2
    assert requests_mock.request_history[1].method == "GET"
    assert requests_mock.request_history[1].url == f"http://db-api/api/node/detection_point/{node_detection_point_uuid}"
