#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
set +a

# Remove the leading backend/app/ from the command line argument so the path works inside of the container.
new_path=${1#backend/app/}

docker-compose up -d
docker exec -e TESTING=yes -e SQL_ECHO=no ace2-ams-api pytest "$new_path" -vv