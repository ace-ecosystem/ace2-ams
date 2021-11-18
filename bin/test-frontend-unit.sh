#!/usr/bin/env bash
TEST_FILE=${1:---}

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
set +a

docker-compose up -d
docker exec ace2-ams-gui npm run test:unit $TEST_FILE --coverage