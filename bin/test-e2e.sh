#!/usr/bin/env bash

# Load the environment variables for the dev containers
ACE2_ENV_PATH="$HOME/.ace2.env"
set -a
source "$ACE2_ENV_PATH"
export TESTING=yes
set +a

# Ensure that the GUI can be built. It is re-built as part of the docker-compose-e2e.yml entrypoint,
# but this lets us see the logs in case there are any errors with the build process.
cd frontend && npm run build || exit $?
cd ..

# Bring up the containers (if they aren't already) in testing mode
docker-compose -f docker-compose.yml -f docker-compose-e2e.yml up -d

# Wait for things to be ready
/usr/bin/env bash bin/wait-for-gui.sh

# Run Cypress
docker exec ace2-ams-gui xvfb-run cypress run --headed --browser chrome