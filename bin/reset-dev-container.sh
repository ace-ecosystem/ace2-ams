#!/usr/bin/env bash

# Set the environment variables for the containers. For now these are written to a file in your home directory
# and then loaded when starting/restarting the dev containers.
ACE2_ENV_PATH="$HOME/.ace2.env"
if [ ! -f "$ACE2_ENV_PATH" ]; then
JWT_SECRET=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
POSTGRES_DB=ace
POSTGRES_USER=ace
POSTGRES_PASSWORD=$(cat /dev/urandom | LC_ALL=C tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

cat > "$ACE2_ENV_PATH" <<- EOF
ACE_DEV=true
COOKIES_SAMESITE=lax
COOKIES_SECURE=False
JWT_ACCESS_EXPIRE_SECONDS=900
JWT_ALGORITHM=HS256
JWT_REFRESH_EXPIRE_SECONDS=43200
JWT_SECRET=$JWT_SECRET
POSTGRES_DB=$POSTGRES_DB
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
DATABASE_API_URL=http://db-api:80/api
DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$POSTGRES_DB
DATABASE_TEST_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/${POSTGRES_DB}_test
SQL_ECHO=yes
EOF
fi

# Load the environment variables for the dev containers
set -a
source "$ACE2_ENV_PATH"
set +a

# Destroy the existing development environment
docker-compose down -v --remove-orphans

# Build the new development environment
docker-compose build

# Start the development environment
docker-compose up -d