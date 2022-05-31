import alembic

from alembic.config import Config
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from api.routes import helpers
from api_models.test import AddTestAlert, AddTestEvent
from core.config import is_in_testing_mode
from db.database import get_db
from seed import seed
from tests import factory


router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


#
# ADD TEST ALERTS
#


def add_test_alerts(alert: AddTestAlert, db: Session = Depends(get_db)):
    # Only proceed if the API is running in TESTING mode
    if is_in_testing_mode():
        for i in range(alert.count):
            factory.alert.create_from_json_file(
                db=db, json_path=f"/app/tests/alerts/{alert.template}", alert_name=f"Manual Alert {i}"
            )

        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=403, detail="Unable to add test alerts when not running in TESTING mode")


helpers.api_route_create(
    router,
    add_test_alerts,
    path="/add_alerts",
    dependencies=[],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The test alerts were added to the database",
        },
        status.HTTP_403_FORBIDDEN: {"description": "Unable to add test alerts when not running in TESTING mode"},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)


#
# ADD TEST EVENTS
#


def add_test_events(event: AddTestEvent, db: Session = Depends(get_db)):
    # Only proceed if the API is running in TESTING mode
    if is_in_testing_mode():
        db_event = factory.event.create_or_read(name=event.name, event_queue=event.queue, status=event.status, db=db)

        for i in range(event.alert_count):
            alert = factory.alert.create_from_json_file(
                db=db, json_path=f"/app/tests/alerts/{event.alert_template}", alert_name=f"Manual Alert {i}"
            )
            alert.event_uuid = db_event.uuid
            db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=403, detail="Unable to add test event when not running in TESTING mode")


helpers.api_route_create(
    router,
    add_test_events,
    path="/add_event",
    dependencies=[],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The test event was added to the database",
        },
        status.HTTP_403_FORBIDDEN: {"description": "Unable to add test event when not running in TESTING mode"},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)


#
# RESET TEST DATABASE
#


def reset_test_database(db: Session = Depends(get_db)):
    # Only proceed if the API is running in TESTING mode
    # NOTE: This functionality is excluded from code coverage since testing it is not possible
    #       with the way that it uses Alembic migrations (and the tests use Alembic migrations)
    if is_in_testing_mode():  # pragma: no cover
        # Use Alembic to downgrade (delete all the database tables) and then upgrade (rebuild the tables)
        config = Config("alembic.ini")
        alembic.command.downgrade(config, "base")
        alembic.command.upgrade(config, "head")

        # Re-seed the database tables so the tests have a default set of data to work with
        seed(db)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=403, detail="Unable to reset the test database when not running in TESTING mode"
        )


helpers.api_route_create(
    router,
    reset_test_database,
    path="/reset_database",
    dependencies=[],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "The test database tables were reset",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Unable to reset the test database when not running in TESTING mode"
        },
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
