#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
set +a

# The e2e tests expect that the containers are reset
/usr/bin/env bash bin/reset-dev-container.sh testing

# Insert the test alert that the e2e tests use into the database
docker exec -e TESTING=yes -e SQL_ECHO=no ace2-ams-api python insert-alerts.py backend/app/tests/alerts/small.json

# Start the e2e tests in the background
docker-compose -f docker-compose.yml -f docker-compose-e2e.yml up -d

# Sleep while the cypress container is still running
printf 'Running Cypress tests'
until ! $(docker top cypress > /dev/null 2>&1); do
    printf '.'
    sleep 1
done

# Print out the cypress container logs
docker logs cypress