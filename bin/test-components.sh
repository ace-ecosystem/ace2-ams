#!/usr/bin/env bash

# Exit if any command fails
set -e

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
export CYPRESS_COVERAGE=true
set +a

# Bring up the containers (if they aren't already) in testing mode
docker compose up -d

# Run Cypress

docker exec -e TZ=America/New_York -e CYPRESS_COVERAGE=true ace2-ams-gui xvfb-run cypress run --component --headless --browser chrome --config-file "cypress.config.ts" --config video=false,screenshotOnRunFailure=false
docker exec ace2-ams-gui npx nyc report --reporter=text-summary

bin/disable-test-mode.sh
