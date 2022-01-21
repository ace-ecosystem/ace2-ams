# ACE2 AMS Development Guide

## Initial setup

This project has VSCode devcontainer support to ensure that anyone working on the project does so in a consistent environment as well as follows the same formatting/styling guidelines.

### Required setup

In order to work within the devcontainer, you will need the following installed on your system:

- [Docker](https://www.docker.com/products/docker-desktop)
- [VSCode](https://code.visualstudio.com/)
- [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) VSCode extension pack

> NOTE: If you are developing in Windows, you will need to make sure that you have WSL 2 set up and properly configured with Docker. That is outside the scope of this documentation, but you can find steps [here](https://docs.docker.com/desktop/windows/wsl/).

## Working in the VSCode devcontainer

When you open the project in VSCode, it will detect the devcontainer configuration and prompt you to reopen it inside of the container:

![Reopen in Container](open-in-container.png)

Once you choose the `Reopen in Container` option, VSCode will work on building the environment. Once it is complete, you can open a terminal within VSCode to interact with the application:

![Terminal](terminal.png)

Any work done on the application should be done through the devcontainer. If you make a change to the devcontainer configuration (found in the `.devcontainer` directory), you can rebuild the devcontainer by clicking on `Dev Container: ACE2 AMS` in the lower-left corner of VSCode and then selecting the `Rebuild Container` option in the menu that opens.

## Updating your hosts file

Your local system will need an entry in the hosts file to properly work with the AMS development environment.

For Mac/Linux, this file is located at `/etc/hosts`.

In Windows, this file is located at `C:\Windows\System32\drivers\etc\hosts`. You will need to open Notepad or another text editor as an Administrator in order to edit the hosts file.

Add the following entry to the file:

```
127.0.0.1 ace2-ams
```

## Starting the application

You can start the application using Docker containers so that it uses hot-reloading anytime you change a file:

```
bin/reset-dev-container.sh
```

This script will generate random passwords for the database user and the secret key used for JWTs. If you need to access these, you can view them in the `$HOME/.ace2.env` file, which configures the environment variables that will be loaded into the database container.

Once the both the frontend and backend development environments are built and started, you can access the components:

- Frontend: [http://ace2-ams:8080](http://ace2-ams:8080)
- Backend API Swagger documentation: [http://localhost:7777/docs](http://localhost:7777/docs)
- Backend API ReDoc documentation: [http://localhost:7777/redoc](http://localhost:7777/redoc)

## Managing NPM packages

You should not directly edit the dependencies or devDependencies inside of `package.json` or anything in `package-lock.json`. **Any changes to packages should be performed via the `npm` command**:

### Install new dependency package

You would install a package like this if it is something the final compiled application needs:

```
npm install <package>
```

### Install new dev dependency package

You would install a package like this if it is only needed during development:

```
npm install -D <package>
```

### Uninstall package

You can uninstall/remove a package regardless of how it was installed by:

```
npm uninstall <package>
```

## Running tests

## Backend

The backend API has a suite of tests performed by Pytest that includes code coverage:

```
bin/test-backend.sh
```

You can run a specific portion of the tests using the same script:

```
bin/test-backend.sh backend/app/tests/api/test_auth_validate.py
```

### Frontend

This frontend has a suite of unit tests performed by [Jest](https://jestjs.io/) and end-to-end tests performed by [Cypress](https://www.cypress.io/).

#### Unit tests

You can execute the unit tests by running:

```
bin/test-frontend-unit.sh
```

#### End-to-end tests

You can execute the end-to-end tests by running:

```
bin/test-e2e.sh
```

##### Test Runner

Cypress also comes with an amazing [Test Runner](https://docs.cypress.io/guides/core-concepts/test-runner) that lets you see and interact with the tests in your local web browser. This can be helpful when writing end-to-end tests to ensure they are working properly as well as any debugging you might need to do.

However, this will need to be performed on your local system ouside of the containers. To do this, you will need to have [Node.js 16](https://nodejs.org/en/download/current/) installed.

**Step 1:** Install Cypress on your host system (this only needs to be done one time):

```
npm install -g cypress@9.3.0
```

**Step 2:** Prep the application to run the tests in interactive mode:

```
bin/test-interactive-e2e.sh
```

**Step 3:** Open the Test Runner on your host system:

```
cd cypress/
cypress open
```

![Test Runner](test-runner.png)

For more information on what you can do with the Test Runner, view the Test Runner [documentation](https://docs.cypress.io/guides/core-concepts/test-runner).
