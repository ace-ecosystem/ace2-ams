import alembic
import os

from alembic.config import Config
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from api.routes import helpers
from db.database import get_db
from seed import seed


router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


#
# RESET TEST DATABASE
#


def reset_test_database(db: Session = Depends(get_db)):
    # Only proceed if the API is running in TESTING mode
    if "TESTING" in os.environ and os.environ["TESTING"].lower() == "yes":
        # Use Alembic to downgrade (delete all the database tables) and then upgrade (rebuild the tables)
        config = Config("alembic.ini")
        alembic.command.downgrade(config, "base")
        alembic.command.upgrade(config, "head")

        # Re-seed the database tables so the tests have a default set of data to work with
        seed()

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
