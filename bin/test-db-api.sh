#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
set +a

# Remove the leading db_api/app/ from the command line argument so the path works inside of the container.
new_path=${1#db_api/app/}

docker-compose up -d
docker exec -e SQL_ECHO=no ace2-ams-db-api pytest "$new_path" -vv

bin/disable-test-mode.sh