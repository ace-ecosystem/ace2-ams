# Analysis Correlation Engine - Alert Management System

ACE2 is comprised of the [Core](https://ace-ecosystem.github.io/ace2-core/) and the Alert Management System. The AMS provides a web interface for analysts to interact with the alerts.

## Quick Start

The AMS comes with a Docker-Compose file to quickly deploy the application in development mode, which includes hot-reloading for both the frontend and backend API:

```
bin/reset-dev-container.sh
```

After the containers are built and running, you can access the components using the following URLs:

- Frontend: [http://localhost:8080](http://localhost:8080)
- Backend API Swagger documentation: [http://localhost:7777/docs](http://localhost:7777/docs)
- Backend API ReDoc documentation: [http://localhost:7777/redoc](http://localhost:7777/redoc)

## Philosophy

For a more in-depth understanding of the philosophy behind ACE, see the talk that John Davison gave on the development of the ACE tool set at BSides Cincinnati in 2015.

[![Automated Detection Strategies](http://img.youtube.com/vi/okMkF-NYCHk/0.jpg)](https://youtu.be/okMkF-NYCHk)
