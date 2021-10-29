from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from typing import Optional, Tuple

from core.auth import hash_password
from db.schemas.alert_queue import AlertQueue
from db.schemas.user import User
from db.schemas.user_role import UserRole


def create_alert(
    client_valid_access_token: TestClient,
    alert_queue: str = "test_queue",
    alert_type: str = "test_type",
    disposition: Optional[str] = None,
    name: Optional[str] = None,
    owner: Optional[str] = None,
    tool: Optional[str] = None,
    tool_instance: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Helper function to create an alert. Returns a tuple of (alert_uuid, analysis_uuid)
    """

    # Create the alert queue if needed. Creating a duplicate will rollback the session.
    alert_queues = client_valid_access_token.get("/api/alert/queue/")
    if not any(q["value"] == alert_queue for q in alert_queues.json()):
        client_valid_access_token.post("/api/alert/queue/", json={"value": alert_queue})

    # Create the alert type if needed. Creating a duplicate will rollback the session.
    alert_types = client_valid_access_token.get("/api/alert/type/")
    if not any(t["value"] == alert_type for t in alert_types.json()):
        client_valid_access_token.post("/api/alert/type/", json={"value": alert_type})

    # Create the alert
    create_json = {"queue": alert_queue, "type": alert_type, "name": name}
    create = client_valid_access_token.post("/api/alert/", json=create_json)

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])

    # Set the disposition if one was given
    if disposition:
        dispositions = client_valid_access_token.get("/api/alert/disposition/")
        if not any(d["value"] == disposition for d in dispositions.json()):
            client_valid_access_token.post(
                "/api/alert/disposition/", json={"value": disposition, "rank": len(dispositions.json()) + 1}
            )

        client_valid_access_token.patch(
            create.headers["Content-Location"], json={"disposition": disposition, "version": get.json()["version"]}
        )

        # Read it back to get the new version
        get = client_valid_access_token.get(create.headers["Content-Location"])

    # Set the owner if one was given
    if owner:
        client_valid_access_token.patch(
            create.headers["Content-Location"], json={"owner": owner, "version": get.json()["version"]}
        )

        # Read it back to get the new version
        get = client_valid_access_token.get(create.headers["Content-Location"])

    # Set the tool if one was given
    if tool:
        tools = client_valid_access_token.get("/api/alert/tool/")
        if not any(t["value"] == tool for t in tools.json()):
            client_valid_access_token.post("/api/alert/tool/", json={"value": tool})

        client_valid_access_token.patch(
            create.headers["Content-Location"], json={"tool": tool, "version": get.json()["version"]}
        )

        # Read it back to get the new version
        get = client_valid_access_token.get(create.headers["Content-Location"])

    # Set the tool instance if one was given
    if tool_instance:
        tool_instances = client_valid_access_token.get("/api/alert/tool/instance/")
        if not any(t["value"] == tool_instance for t in tool_instances.json()):
            client_valid_access_token.post("/api/alert/tool/instance/", json={"value": tool_instance})

        client_valid_access_token.patch(
            create.headers["Content-Location"], json={"tool_instance": tool_instance, "version": get.json()["version"]}
        )

        # Read it back to get the new version
        get = client_valid_access_token.get(create.headers["Content-Location"])

    return get.json()["uuid"], get.json()["analysis"]["uuid"]


def create_event(client_valid_access_token: TestClient, name: str, status: str = "OPEN") -> str:
    """
    Helper function to create an event. Returns the event UUID.
    """

    # Create an event status and remediation
    client_valid_access_token.post("/api/event/status/", json={"value": status})

    # Create the event
    create = client_valid_access_token.post("/api/event/", json={"name": name, "status": status})

    # Read it back
    get = client_valid_access_token.get(create.headers["Content-Location"])
    return get.json()["uuid"]


def create_test_user(db: Session, username: str, password: str):
    # Create an alert queue
    alert_queue = AlertQueue(value="test_queue")
    db.add(alert_queue)

    # Create a user role
    user_role = UserRole(value="test_role")
    db.add(user_role)

    # Create a user
    user = User(
        default_alert_queue=alert_queue,
        display_name="John Doe",
        email="john@test.com",
        password=hash_password(password),
        roles=[user_role],
        username=username,
    )
    db.add(user)
