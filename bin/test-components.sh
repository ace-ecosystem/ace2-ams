#!/usr/bin/env bash

# Exit if any command fails
set -e

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
# export CYPRESS_INSTALL_BINARY=10.0.2
set +a

# Bring up the containers (if they aren't already) in testing mode
docker-compose up -d

# Run Cypress

docker exec -e TZ=America/New_York ace2-ams-gui xvfb-run node_modules/.bin/cypress run --component --headed --browser chrome

bin/disable-test-mode.sh
