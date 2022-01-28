#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
set +a

# Remove the leading frontend/ from the command line argument so the path works inside of the container.
TEST_FILE=${1#frontend/}

docker-compose up -d
# docker exec ace2-ams-gui npm run test:unit "$TEST_FILE" -- --coverage
docker exec -e VITE_TESTING=yes ace2-ams-gui npm run test:unit "$TEST_FILE"