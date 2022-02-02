#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
set +a

# Bring up the containers (if they aren't already) in testing mode
docker-compose -f docker-compose.yml -f docker-compose-e2e.yml up -d

# Wait for the GUI to be compiled before running Cypress
printf "Waiting for GUI to compile"
until $(curl --output /dev/null --silent --head --fail http://ace2-ams:8080); do
    printf "."
    sleep 1
done

# Run Cypress
docker exec ace2-ams-gui xvfb-run cypress run --headed --browser chrome