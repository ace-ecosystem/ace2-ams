#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
set +a

# Start the entire application and then pause until the database is accessible.
# NOTE: If you changed the mapped port for the "db" service in the docker-compose.yml
# file, you will need to update it below in the "while" loop as well.
docker-compose up -d
while !</dev/tcp/localhost/6666; do sleep 1; done;

# Create the database revision
docker exec ace2-ams-api alembic upgrade head