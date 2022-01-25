# Create the "ace" and "ace_test" databases and enable the required extensions
for db in ace ace_test
do
    echo "SELECT 'CREATE DATABASE $db' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db')\gexec" | psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER"

    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$db" -c "CREATE EXTENSION IF NOT EXISTS pg_trgm"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$db" -c "CREATE EXTENSION IF NOT EXISTS pgcrypto"
done

# Create a script to truncate all of the ace_test tables (used during the E2E tests)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE OR REPLACE FUNCTION truncate_test_tables() RETURNS void AS \$\$
    DECLARE
        dbname VARCHAR := current_database();
        statements CURSOR FOR
            SELECT tablename FROM pg_tables
            WHERE tableowner = 'ace' AND schemaname = 'public';
    BEGIN
        IF position('ace_test' in dbname) > 0 THEN
            FOR stmt IN statements LOOP
                EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
            END LOOP;
        END IF;
    END;
    \$\$ LANGUAGE plpgsql;
EOSQL