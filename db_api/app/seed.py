import os
import sys
import yaml

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta

from core.auth import hash_password
from core.config import is_in_testing_mode
from db.database import get_db
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.event_remediation import EventRemediation
from db.schemas.event_severity import EventSeverity
from db.schemas.event_source import EventSource
from db.schemas.event_status import EventStatus
from db.schemas.event_type import EventType
from db.schemas.event_vector import EventVector
from db.schemas.metadata_directive import MetadataDirective
from db.schemas.observable_relationship_type import ObservableRelationshipType
from db.schemas.observable_type import ObservableType
from db.schemas.queue import Queue
from db.schemas.seed import Seed
from db.schemas.submission_type import SubmissionType
from db.schemas.threat_type import ThreatType
from db.schemas.user import User
from db.schemas.user_role import UserRole


# NOTE: The print statements in this file show up in the Docker logs when you run:
# docker logs ace2-gui-backend


def add_queueable_values(db: Session, db_table: DeclarativeMeta, queues: dict, data: dict, key: str, print_value: str):
    # Transform the data into a dictionary where the keys are the individual values from the config
    # and the values are lists of which queue they belong to.
    transformed_data: dict[str, list[str]] = {}

    for queue in data[key]:
        for value in data[key][queue]:
            if value not in transformed_data:
                transformed_data[value] = []

            transformed_data[value].append(queue)

    for value in transformed_data:
        db_obj = db_table(value=str(value))
        for queue in transformed_data[value]:
            db_obj.queues.append(queues[queue])
            print(f"Adding {print_value} for {queue} queue: {value}")
        db.add(db_obj)


def seed(db: Session):
    # Quit early if the database was already seeded
    if db.execute(select(Seed)).one_or_none():
        print("The database was already seeded!")
        sys.exit()

    # Quit early if the config file does not exist
    if not os.path.exists("etc/defaults.yml"):
        print("etc/defaults.yml does not exist!")
        sys.exit()

    # Load the data from the config file
    data = None
    with open("etc/defaults.yml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)

    # Quit early if the config file is empty
    if data is None:
        print("etc/defaults.yml is empty!")
        sys.exit()

    # Add the queues to the database
    queues = {}
    if "queue" in data:
        for value in data["queue"]:
            queues[value] = Queue(value=value)
            db.add(queues[value])
            print(f"Adding queue: {value}")

    # Add the rest of the objects from the config into the database
    if "alert_disposition" in data:
        for rank, value in enumerate(data["alert_disposition"]):
            db.add(AlertDisposition(rank=rank, value=value))
            print(f"Adding alert disposition: {rank}:{value}")

    if "directive" in data:
        for directive in data["directive"]:
            db.add(MetadataDirective(value=directive["value"], description=directive["description"]))
            print(f"Adding directive: {value}")

    if "event_prevention_tool" in data:
        add_queueable_values(
            db=db,
            db_table=EventPreventionTool,
            queues=queues,
            data=data,
            key="event_prevention_tool",
            print_value="event prevention tool",
        )

    if "event_remediation" in data:
        add_queueable_values(
            db=db,
            db_table=EventRemediation,
            queues=queues,
            data=data,
            key="event_remediation",
            print_value="event remediation",
        )

    if "event_severity" in data:
        add_queueable_values(
            db=db,
            db_table=EventSeverity,
            queues=queues,
            data=data,
            key="event_severity",
            print_value="event severity",
        )

    if "event_source" in data:
        add_queueable_values(
            db=db, db_table=EventSource, queues=queues, data=data, key="event_source", print_value="event source"
        )

    if "event_status" in data:
        add_queueable_values(
            db=db, db_table=EventStatus, queues=queues, data=data, key="event_status", print_value="event status"
        )

    if "event_type" in data:
        add_queueable_values(
            db=db, db_table=EventType, queues=queues, data=data, key="event_type", print_value="event type"
        )

    if "event_vector" in data:
        add_queueable_values(
            db=db, db_table=EventVector, queues=queues, data=data, key="event_vector", print_value="event vector"
        )

    if "observable_relationship_type" in data:
        for value in data["observable_relationship_type"]:
            db.add(ObservableRelationshipType(value=value))
            print(f"Adding node relationship type: {value}")

    if "threat_type" in data:
        add_queueable_values(
            db=db,
            db_table=ThreatType,
            queues=queues,
            data=data,
            key="threat_type",
            print_value="node threat type",
        )

    if "observable_type" in data:
        for value in data["observable_type"]:
            db.add(ObservableType(value=value))
            print(f"Adding observable type: {value}")

    if "submission_type" in data:
        for value in data["submission_type"]:
            db.add(SubmissionType(value=value))
            print(f"Adding submission type: {value}")

    user_roles = {}
    if "user_role" in data:
        for value in data["user_role"]:
            user_roles[value] = UserRole(value=value)
            db.add(user_roles[value])
            print(f"Adding user role: {value}")

    if "user" in data:
        for user in data["user"]:
            db_user = User(
                default_alert_queue=queues[user["default_alert_queue"]],
                default_event_queue=queues[user["default_event_queue"]],
                display_name=user["display_name"],
                email=user["email"],
                password=hash_password(user["password"]),
                username=user["username"],
            )
            for user_role in user["roles"]:
                db_user.roles.append(user_roles[user_role])

            db.add(db_user)
            print(f"Adding user: {user['username']}")

    # Add a record saying the database was seeded
    db.add(Seed())

    # Commit all of the changes
    db.commit()


if __name__ == "__main__" and not is_in_testing_mode():
    db: Session = next(get_db())
    seed(db)
