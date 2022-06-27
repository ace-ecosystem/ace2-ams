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
docker compose -f docker-compose.yml up -d

# Wait for things to be ready
docker exec ace2-ams-gui bin/wait-for-gui.sh

# Run Cypress
docker exec ace2-ams-gui xvfb-run cypress run --e2e --headless --browser chrome --config-file "cypress.config.ts" --config video=false,screenshotOnRunFailure=false

bin/disable-test-mode.sh
