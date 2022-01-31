#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
set +a

# Bring up the containers (if they aren't already) in testing mode
docker-compose -f docker-compose.yml up -d

# Run Cypress
docker exec ace2-ams-gui xvfb-run cypress run --headed --browser chrome

# Disable TESTING mode
/usr/bin/env bash bin/disable-test-mode.sh