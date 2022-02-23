import os
import sys
import yaml

from sqlalchemy.orm import Session

from core.auth import hash_password
from core.config import is_in_testing_mode
from db import crud
from db.database import get_db
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.alert_type import AlertType
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.event_remediation import EventRemediation
from db.schemas.event_risk_level import EventRiskLevel
from db.schemas.event_source import EventSource
from db.schemas.event_status import EventStatus
from db.schemas.event_type import EventType
from db.schemas.event_vector import EventVector
from db.schemas.node_threat_type import NodeThreatType
from db.schemas.observable_type import ObservableType
from db.schemas.queue import Queue
from db.schemas.user import User
from db.schemas.user_role import UserRole


# NOTE: The print statements in this file show up in the Docker logs when you run:
# docker logs ace2-gui-backend


def seed(db: Session):
    # Quit early if the config file does not exist
    if not os.path.exists("etc/defaults.yml"):
        print("etc/defaults.yml does not exist!")
        sys.exit()

    data = None
    with open("etc/defaults.yml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    # Quit early if the config file is empty
    if data is None:
        print("etc/defaults.yml is empty!")
        sys.exit()

    # Add the objects to the database but only if their respective tables do not have any items already.
    if "alert_disposition" in data and not crud.read_all(db_table=AlertDisposition, db=db):
        for rank, value in enumerate(data["alert_disposition"]):
            db.add(AlertDisposition(rank=rank, value=value))
            print(f"Adding alert disposition: {rank}:{value}")

    if not crud.read_all(db_table=Queue, db=db):
        if "queue" in data:
            # Make sure there is always a "default" queue
            if "default" not in data["queue"]:
                data["queue"].append("default")

            for value in data["queue"]:
                db.add(Queue(value=value))
                print(f"Adding queue: {value}")
        else:
            # Make sure there is always a "default" queue
            db.add(Queue(value="default"))
            print("Adding queue: default")

    if "alert_type" in data and not crud.read_all(db_table=AlertType, db=db):
        for value in data["alert_type"]:
            db.add(AlertType(value=value))
            print(f"Adding alert type: {value}")

    if "event_prevention_tool" in data and not crud.read_all(db_table=EventPreventionTool, db=db):
        for value in data["event_prevention_tool"]:
            db.add(EventPreventionTool(value=value))
            print(f"Adding event prevention tool: {value}")

    if "event_remediation" in data and not crud.read_all(db_table=EventRemediation, db=db):
        for value in data["event_remediation"]:
            db.add(EventRemediation(value=value))
            print(f"Adding event remediation: {value}")

    if "event_risk_level" in data and not crud.read_all(db_table=EventRiskLevel, db=db):
        for value in data["event_risk_level"]:
            db.add(EventRiskLevel(value=value))
            print(f"Adding event risk level: {value}")

    if "event_source" in data and not crud.read_all(db_table=EventSource, db=db):
        for value in data["event_source"]:
            db.add(EventSource(value=value))
            print(f"Adding event source: {value}")

    if "event_status" in data and not crud.read_all(db_table=EventStatus, db=db):
        for value in data["event_status"]:
            db.add(EventStatus(value=value))
            print(f"Adding event status: {value}")

    if "event_type" in data and not crud.read_all(db_table=EventType, db=db):
        for value in data["event_type"]:
            db.add(EventType(value=value))
            print(f"Adding event type: {value}")

    if "event_vector" in data and not crud.read_all(db_table=EventVector, db=db):
        for value in data["event_vector"]:
            db.add(EventVector(value=value))
            print(f"Adding event vector: {value}")

    if "node_threat_type" in data and not crud.read_all(db_table=NodeThreatType, db=db):
        for value in data["node_threat_type"]:
            db.add(NodeThreatType(value=value))
            print(f"Adding node threat type: {value}")

    if "observable_type" in data and not crud.read_all(db_table=ObservableType, db=db):
        for value in data["observable_type"]:
            db.add(ObservableType(value=value))
            print(f"Adding observable type: {value}")

    if not crud.read_all(db_table=UserRole, db=db):
        if "user_role" in data:
            # Make sure there is always an "admin" role
            if "admin" not in data["user_role"]:
                data["user_role"].append("admin")

            for value in data["user_role"]:
                db.add(UserRole(value=value))
                print(f"Adding user role: {value}")
        else:
            # Make sure there is always an "admin" role
            db.add(UserRole(value="admin"))
            print("Adding user role: admin")

    # Add an "analyst" user if there are no existing users
    if not crud.read_all(db_table=User, db=db):
        # Commit the database changes so that they can be used to create the analyst user
        crud.commit(db)

        db.add(
            User(
                default_alert_queue=crud.read_by_value(value="default", db_table=Queue, db=db),
                default_event_queue=crud.read_by_value(value="default", db_table=Queue, db=db),
                display_name="Analyst",
                email="analyst@fake.com",
                password=hash_password("analyst"),
                roles=crud.read_by_values(values=["admin"], db_table=UserRole, db=db),
                username="analyst",
            )
        )
        db.add(
            User(
                default_alert_queue=crud.read_by_value(value="default", db_table=Queue, db=db),
                default_event_queue=crud.read_by_value(value="default", db_table=Queue, db=db),
                display_name="Analyst Alice",
                email="alice@alice.com",
                password=hash_password("analyst"),
                roles=crud.read_by_values(values=["admin"], db_table=UserRole, db=db),
                username="alice",
            )
        )
        db.add(
            User(
                default_alert_queue=crud.read_by_value(value="default", db_table=Queue, db=db),
                default_event_queue=crud.read_by_value(value="default", db_table=Queue, db=db),
                display_name="Analyst Bob",
                email="bob@bob.com",
                password=hash_password("analyst"),
                roles=crud.read_by_values(values=["admin"], db_table=UserRole, db=db),
                username="bob",
            )
        )
        print("Adding user: analyst")

    # Commit all of the changes
    crud.commit(db)


if __name__ == "__main__":
    # Don't seed the database automatically if running in TESTING mode
    if not is_in_testing_mode():
        db: Session = next(get_db())
        seed(db)
