# Analysis Correlation Engine - Alert Management System

ACE2 is comprised of the [Core](https://ace-ecosystem.github.io/ace2-core/) and the Alert Management System. The AMS provides a web interface for analysts to interact with the alerts.

## Quick Start

Your local system will need an entry in the hosts file to properly work with the AMS development environment.

For Mac/Linux, this file is located at `/etc/hosts`.

In Windows, this file is located at `C:\Windows\System32\drivers\etc\hosts`. You will need to open Notepad or another text editor as an Administrator in order to edit the hosts file.

Add the following entry to the file:

```
127.0.0.1 ace2-ams
```

With your host file updated, you can use the helper script to reset and build the local AMS development environment that includes hot-reloading for both the frontend and APIs:

```
bin/reset-dev-container.sh
```

After the containers are built and running, you can access the components using the following URLs:

- Frontend: [http://ace2-ams:8080](http://ace2-ams:8080)
- Database API Swagger documentation: [http://localhost:8888/docs](http://localhost:8888/docs)
- Database API ReDoc documentation: [http://localhost:8888/redoc](http://localhost:8888/redoc)
- GUI API Swagger documentation: [http://localhost:7777/docs](http://localhost:7777/docs)
- GUI API ReDoc documentation: [http://localhost:7777/redoc](http://localhost:7777/redoc)

## Philosophy

For a more in-depth understanding of the philosophy behind ACE, see the talk that John Davison gave on the development of the ACE tool set at BSides Cincinnati in 2015.

[![Automated Detection Strategies](http://img.youtube.com/vi/okMkF-NYCHk/0.jpg)](https://youtu.be/okMkF-NYCHk)
