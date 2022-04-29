import alembic
import pytest

from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api_models.queue import QueueCreate
from api_models.user import UserCreate
from api_models.user_role import UserRoleCreate
from db import crud
from db.database import engine, get_db
from main import app


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """
    This fixture applies the Alembic database migrations at the beginning of a Pytest session and performs
    a downgrade (effectively removing all database tables) at the very end of the session.
    """

    config = Config("alembic.ini")

    alembic.command.downgrade(config, "base")
    alembic.command.upgrade(config, "head")

    # Add the analyst user so API calls that create history entries have a valid user to link to.
    session_db = next(get_db())

    # TODO: Use the user factory function instead
    crud.queue.create(model=QueueCreate(value="external"), db=session_db)
    crud.user_role.create(model=UserRoleCreate(value="analyst"), db=session_db)
    crud.user.create(
        model=UserCreate(
            default_alert_queue="external",
            default_event_queue="external",
            display_name="Analyst",
            email="analyst@test.local",
            password="asdfasdf",
            roles=["analyst"],
            username="analyst",
        ),
        db=session_db,
    )
    session_db.commit()

    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture()
def db():
    """
    This fixture creates a nested database transaction for each test that uses it. When the test is
    complete, the transaction is rolled back so that the database is in the same state as prior to the test.

    Most tests will not need to use this fixture directly, as they will use it indirectly via the client fixture.
    """

    # Connect to the database and begin a nested transaction.
    connection = engine.connect()
    connection.begin()
    session = Session(bind=connection)

    yield session

    # Close the session and the connection. The transaction is automatically rolled back.
    session.close()
    connection.close()


@pytest.fixture()
def client(db):
    """
    This fixture supplies a TestClient to use for testing API endpoints. It overrides the get_db
    function so that it uses the db fixture and its transaction rollback logic. The database
    will be rolled back to its original state after the test is complete.
    """

    # If "db" were a regular function instead of a fixture and we used that for dependency_overrides
    # instead of the override_get_db sub-function that yields the db fixture, the database transaction
    # would be rolled back after every database query (even within the same test).
    def override_get_db():
        yield db

    # Override the get_db function to use the testing db fixture so that every
    # test gets its own transaction that is rolled back when it completes.
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c
