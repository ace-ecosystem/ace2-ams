#!/usr/bin/env bash

# Exit if any command fails
set -e

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
set +a

# Bring up the containers (if they aren't already) in testing mode
docker-compose up -d

# Run Cypress
docker exec -e TZ=America/New_York ace2-ams-gui xvfb-run cypress run-ct --headed --browser chrome

bin/disable-test-mode.sh