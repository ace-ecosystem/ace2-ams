import alembic
import logging

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool

from core.config import get_settings, is_in_testing_mode

# Load the database schemas so that Alembic knows what it needs to create/update
from db import schemas
from db.database import Base

# Alembic Config object, which provides access to values within the .ini file
config = alembic.context.config

# Interpret the config file for logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in "online" mode
    """

    # Handle database configuration for running tests
    if is_in_testing_mode():
        database_url = get_settings().database_test_url
    else:
        database_url = get_settings().database_url

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", database_url)

    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(connection=connection, target_metadata=Base.metadata)

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in "offline" mode.
    """

    if is_in_testing_mode():
        database_url = get_settings().database_test_url
    else:
        database_url = get_settings().database_url

    alembic.context.configure(url=database_url)

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
