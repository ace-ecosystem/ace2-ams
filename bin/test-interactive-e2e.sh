#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
set +a

# The e2e tests expect that the containers are reset
/usr/bin/env bash bin/reset-dev-container.sh

# Insert the test alert that the e2e tests use into the database
/usr/bin/env bash bin/insert-alerts.sh backend/app/tests/alerts/small.json

printf "\nYou can now open Cypress on your host system\n"