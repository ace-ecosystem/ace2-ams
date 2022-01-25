#!/usr/bin/env bash

if [ "$1" = "testing" ]; then
    TESTING="yes"
else
    TESTING="no"
fi

# Load the environment variables for the dev containers
set -a
source "$ACE2_ENV_PATH"
# Figure out if the containers need to be reset in TESTING mode
export TESTING=$TESTING
set +a

bin/stop-dev-container.sh
docker-compose -f docker-compose.yml up -d