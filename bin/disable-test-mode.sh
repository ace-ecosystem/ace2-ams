#!/usr/bin/env bash

ACE2_ENV_PATH="$HOME/.ace2.env"

# Load the environment variables for the dev containers
set -a
source "$ACE2_ENV_PATH"
export TESTING=no
set +a

docker-compose -f docker-compose.yml up -d