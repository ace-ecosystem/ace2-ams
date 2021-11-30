import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

database_url = get_settings().database_url
if "TESTING" in os.environ and os.environ["TESTING"]:
    database_url = f"{database_url}_test"

echo_value = False
if "SQL_ECHO" in os.environ and os.environ["SQL_ECHO"] == "yes":
    echo_value = True

engine = create_engine(database_url, echo=echo_value)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
