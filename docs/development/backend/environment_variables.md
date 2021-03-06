# Environment Variables

The backend container relies on a number of environment variables. For the development environment, these are automatically generated by the `bin/reset-dev-container.sh` script and stored inside of the `.ace2.env` file inside of your home directory.

These environment variables will need to be set by other means if you are running this application in production.

## Database API variables

These variables are used by the database API application.

- **ACE_DEV**: If set (to anything), the application will run in development-mode, which means that the Alembic database migrations will be applied and the database seeded with basic information automatically when the application starts. This is enabled by default for the development environment.
- **DATABASE_URL**: The connection string used to connect to the PostgreSQL server. It should be in the form of `postgresql://user:password@hostname[:port]/dbname`.
- **DATABASE_TEST_URL**: The connection string used to connect to the test PostgreSQL server. It should be in the form of `postgresql://user:password@hostname[:port]/dbname`.
- **SQL_ECHO**: If set (to anything), SQLAlchemy will be configured to echo all queries to the console. You can view the queries in the Docker logs for the `ace2-ams-api` container. This is enabled by default for the development environment.
- **TESTING**: If set to "yes", this instructs the API to utilize the test database (such as when running the unit tests).

## GUI API variables

These variables are used by the GUI API application.

- **COOKIES_SAMESITE**: The `SameSite` value to use when sending cookies. The development environment uses `lax`. Defaults to `lax`.
- **COOKIES_SECURE**: True/False whether or not you want to require HTTPS when sending cookies. The development environment uses `False`. Defaults to `True`.
- **DATABASE_API_URL**: The base URL to reach the database API. The development environment uses `http://db-api/api` by default.
- **JWT_ACCESS_EXPIRE_SECONDS**: The number of seconds after which an access token will expire. The development environment uses `900` (15 minutes) by default.
- **JWT_ALGORITHM**: Sets the algorithm to use for signing the tokens. The development environment uses `HS256` by default.
- **JWT_REFRESH_EXPIRE_SECONDS**: The number of seconds after which a refresh token will expire. The development environment uses `43200` (12 hours) by default.
- **JWT_SECRET**: The secret key/password to use when signing and decoding tokens. The development environment generates `a random 32 character string`.
- **SQL_ECHO**: If set (to anything), SQLAlchemy will be configured to echo all queries to the console. You can view the queries in the Docker logs for the `ace2-ams-api` container. This is enabled by default for the development environment.

## PostgreSQL container variables

These variables are used by the PostgreSQL server container to initialize the database.

- **POSTGRES_DB**: The name of the database to create. The development environment uses `ace`.
- **POSTGRES_USER**: The user to use to connect to the PostgreSQL server. The development environment uses `ace`.
- **POSTGRES_PASSWORD**: The password to use to connect to the PostgreSQL server. The development environment generates `a random 32 character string`.
