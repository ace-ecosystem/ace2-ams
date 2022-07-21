#!/bin/bash

# /app/prestart.sh is functionality built into the base Docker image.
# See https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker for more details.

# Run the database migrations and seed if running in DEV mode
if [ -n "$ACE_DEV" ]; then
    alembic upgrade head

    python /app/seed.py
fi
