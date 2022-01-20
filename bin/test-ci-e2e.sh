#!/usr/bin/env bash

# The e2e tests expect that the containers are reset
/usr/bin/env bash bin/reset-dev-container.sh

# Insert the test alert that the e2e tests use into the database
/usr/bin/env bash bin/insert-alerts.sh backend/app/tests/alerts/small.json

# Start the e2e tests
docker-compose -f docker-compose.yml -f docker-compose-e2e-ci.yml up --exit-code-from cypress