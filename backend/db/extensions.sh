# Create the "ace" and "ace_test" databases and enable the required extensions
for db in ace ace_test
do
    echo "SELECT 'CREATE DATABASE $db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db')\gexec" | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER"

    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$db" -c "CREATE EXTENSION IF NOT EXISTS pg_trgm"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$db" -c "CREATE EXTENSION IF NOT EXISTS pgcrypto"
done