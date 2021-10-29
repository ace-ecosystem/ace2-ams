# ACE2 GUI
The ACE2 Alert Management System (AMS) is comprised of three main components: a PostgreSQL database, a FastAPI backend, and a Vue.js frontend.

## Documentation
The project's documentation is available at https://ace-ecosystem.github.io/ace2-gui/.

## Project setup for development
The included `docker-compose.yml` file runs the full application in development mode. This uses volumes to your local source code directories and enables hot-reload for the Vue.js and FastAPI applications. There are various scripts included to simplify some of the docker-compose commands.

To rebuild the development environment (which will also erase your development database):
```
bin/reset-dev-container.sh
```

This script will generate random passwords for the database user. If you need to access these, you can view them in the `$HOME/.ace2.env` file, which configures the environment variables that will be loaded into the database container.

Once the development environment is built and started, you can access the components:

* Backend API Swagger documentation: http://localhost:8888/docs
* Backend API ReDoc documentation: http://localhost:8888/redoc