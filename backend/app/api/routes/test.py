import alembic

from alembic.config import Config
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from api.models.test import AddTestAlert
from api.routes import helpers
from core.config import is_in_testing_mode
from db.database import get_db
from seed import seed
from tests import helpers as test_helpers


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
            test_helpers.create_alert_from_json_file(
                db=db, json_path=f"/app/tests/alerts/{alert.template}", alert_name=f"Manual Alert {i}"
            )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=403, detail="Unable to reset the test database when not running in TESTING mode"
        )


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
# RESET TEST DATABASE
#


def reset_test_database(db: Session = Depends(get_db)):
    # Only proceed if the API is running in TESTING mode
    if is_in_testing_mode():
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
