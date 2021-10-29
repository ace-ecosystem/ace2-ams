import pytest
import uuid

from fastapi import status

from tests.api.observable_instance.test_create import create_alert
from tests.api.node import (
    INVALID_UPDATE_FIELDS,
    NONEXISTENT_FIELDS,
    VALID_DIRECTIVES,
    VALID_TAGS,
    VALID_THREAT_ACTOR,
    VALID_THREATS,
)


#
# INVALID TESTS
#


@pytest.mark.parametrize(
    "key,value",
    [
        ("context", 123),
        ("context", ""),
        ("performed_analysis_uuids", 123),
        ("performed_analysis_uuids", "abc"),
        ("performed_analysis_uuids", [123]),
        ("performed_analysis_uuids", [None]),
        ("performed_analysis_uuids", [""]),
        ("performed_analysis_uuids", ["abc"]),
        ("redirection_uuid", 123),
        ("redirection_uuid", ""),
        ("redirection_uuid", "abc"),
        ("time", None),
        ("time", ""),
        ("time", "Monday"),
        ("time", "2022-01-01"),
    ],
)
def test_update_invalid_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{uuid.uuid4()}",
        json={
            key: value,
            "version": str(uuid.uuid4()),
        },
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


@pytest.mark.parametrize(
    "key,value",
    INVALID_UPDATE_FIELDS,
)
def test_update_invalid_node_fields(client_valid_access_token, key, value):
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{uuid.uuid4()}",
        json={
            "version": str(uuid.uuid4()),
            key: value,
        },
    )
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert key in update.text


def test_update_invalid_uuid(client_valid_access_token):
    update = client_valid_access_token.patch("/api/observable/instance/1", json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_invalid_version(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Make sure you cannot update it using an invalid version
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={"version": str(uuid.uuid4())})
    assert update.status_code == status.HTTP_409_CONFLICT


def test_update_nonexistent_performed_analysis_uuids(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED

    # Make sure you cannot update it to use a nonexistent analysis UUID
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"performed_analysis_uuids": [str(uuid.uuid4())], "version": version}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_redirection_uuid(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])
    assert create.status_code == status.HTTP_201_CREATED

    # Make sure you cannot update it to use a nonexistent redirection UUID
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"redirection_uuid": str(uuid.uuid4()), "version": version}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "key,value",
    NONEXISTENT_FIELDS,
)
def test_update_nonexistent_node_fields(client_valid_access_token, key, value):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Make sure you cannot update it to use a nonexistent node field value
    update = client_valid_access_token.patch(create.headers["Content-Location"], json={key: value, "version": version})
    assert update.status_code == status.HTTP_404_NOT_FOUND


def test_update_nonexistent_uuid(client_valid_access_token):
    update = client_valid_access_token.patch(
        f"/api/observable/instance/{uuid.uuid4()}", json={"version": str(uuid.uuid4())}
    )
    assert update.status_code == status.HTTP_404_NOT_FOUND


#
# VALID TESTS
#


def test_update_performed_analysis_uuids(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["performed_analysis_uuids"] == []

    # Create a child analysis
    child_analysis_uuid = str(uuid.uuid4())
    analysis_create = client_valid_access_token.post("/api/analysis/", json={"uuid": child_analysis_uuid})

    # Read the analysis back to get its current version
    get_analysis = client_valid_access_token.get(analysis_create.headers["Content-Location"])
    initial_version = get_analysis.json()["version"]

    # Update the performed analyses
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"performed_analysis_uuids": [child_analysis_uuid], "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["performed_analysis_uuids"] == [child_analysis_uuid]
    assert get.json()["version"] != version

    # Read the analysis back. By updating the observable instance and setting its performed_analysis_uuids, you should
    # be able to read the analysis back and see the observable instance listed as its parent_observable_uuid even
    # though it was not explicitly added.
    get_analysis = client_valid_access_token.get(analysis_create.headers["Content-Location"])
    assert get_analysis.json()["parent_observable_uuid"] == get.json()["uuid"]

    # Additionally, adding the observable instance as the parent should trigger the analysis to have a new version.
    assert get_analysis.json()["version"] != initial_version


def test_update_redirection_uuid(client_valid_access_token):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["redirection_uuid"] is None

    # Create a second observable instance to use for redirection
    redirection_uuid = str(uuid.uuid4())
    create2_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "uuid": redirection_uuid,
        "value": "test",
        "version": version,
    }
    client_valid_access_token.post("/api/observable/instance/", json=[create2_json])

    # Update the redirection UUID
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"redirection_uuid": redirection_uuid, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["redirection_uuid"] == redirection_uuid
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_DIRECTIVES,
)
def test_update_valid_node_directives(client_valid_access_token, values):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create the directives. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/directive/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"directives": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["directives"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_TAGS,
)
def test_update_valid_node_tags(client_valid_access_token, values):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["tags"] == []

    # Create the tags. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/tag/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"tags": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["tags"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "value",
    VALID_THREAT_ACTOR,
)
def test_update_valid_node_threat_actor(client_valid_access_token, value):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["threat_actor"] is None

    # Create the threat actor
    if value:
        client_valid_access_token.post("/api/node/threat_actor/", json={"value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"threat_actor": value, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    if value:
        assert get.json()["threat_actor"]["value"] == value
    else:
        assert get.json()["threat_actor"] is None

    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "values",
    VALID_THREATS,
)
def test_update_valid_node_threats(client_valid_access_token, values):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()["directives"] == []

    # Create a threat type
    client_valid_access_token.post("/api/node/threat/type/", json={"value": "test_type"})

    # Create the threats. Need to only create unique values, otherwise the database will return a 409
    # conflict exception and will roll back the test's database session (causing the test to fail).
    for value in list(set(values)):
        client_valid_access_token.post("/api/node/threat/", json={"types": ["test_type"], "value": value})

    # Update the node
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"threats": values, "version": version}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert len(get.json()["threats"]) == len(list(set(values)))
    assert get.json()["version"] != version


@pytest.mark.parametrize(
    "key,initial_value,updated_value",
    [
        ("context", None, "test"),
        ("context", "test", None),
        ("context", "test", "test"),
        ("time", "2021-01-01T00:00:00+00:00", 1640995200),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01T00:00:00Z"),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00"),
        ("time", "2021-01-01T00:00:00+00:00", "2022-01-01 00:00:00.000000"),
        ("time", "2021-01-01T00:00:00+00:00", "2021-12-31 19:00:00-05:00"),
    ],
)
def test_update(client_valid_access_token, key, initial_value, updated_value):
    # Create an alert
    alert_uuid, analysis_uuid = create_alert(client_valid_access_token=client_valid_access_token)

    # Create an observable type
    client_valid_access_token.post("/api/observable/type/", json={"value": "test_type"})

    # Create an observable instance
    version = str(uuid.uuid4())
    create_json = {
        "alert_uuid": alert_uuid,
        "parent_analysis_uuid": analysis_uuid,
        "type": "test_type",
        "value": "test",
        "version": version,
    }
    create_json[key] = initial_value
    create = client_valid_access_token.post("/api/observable/instance/", json=[create_json])

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    assert get.json()[key] == initial_value

    # Update it
    update = client_valid_access_token.patch(
        create.headers["Content-Location"], json={"version": version, key: updated_value}
    )
    assert update.status_code == status.HTTP_204_NO_CONTENT

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # If the test is for time, make sure that the retrieved value matches the proper UTC timestamp
    if key == "time":
        assert get.json()[key] == "2022-01-01T00:00:00+00:00"
    else:
        assert get.json()[key] == updated_value

    assert get.json()["version"] != version
