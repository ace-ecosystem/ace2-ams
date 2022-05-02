import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from typing import Generator

from core.config import get_settings, is_in_testing_mode

database_url = get_settings().database_url
if is_in_testing_mode():
    database_url = get_settings().database_test_url

echo_value = False
if "SQL_ECHO" in os.environ and os.environ["SQL_ECHO"].lower() == "yes":
    echo_value = True

engine = create_engine(database_url, echo=echo_value)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
