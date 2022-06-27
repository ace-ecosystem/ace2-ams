#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
set +a

# Bring up the containers (if they aren't already) in testing mode
docker compose -f docker-compose.yml up -d

printf "\nYou can now open Cypress on your host system\n"
printf "Exit test mode when you are finished: bin/disable-test-mode.sh\n"