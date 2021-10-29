import alembic
import pytest

from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.database import engine, get_db
from main import app


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """
    This fixture applies the Alembic database migrations at the beginning of a Pytest session and performs
    a downgrade (effectively removing all database tables) at the very end of the session.
    """

    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
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


@pytest.fixture()
def client_valid_access_token(client, monkeypatch):
    """
    This fixture is the "client" fixture with a patched validate_access_token function so that it always validates.
    """

    def mock_validate_access_token():
        return "analyst"

    # Due to how imports work, patching __code__ accounts for all cases for how the function is imported and used.
    monkeypatch.setattr("core.auth.validate_access_token.__code__", mock_validate_access_token.__code__)

    yield client
