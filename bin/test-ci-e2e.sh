#!/usr/bin/env bash

# Wait for the GUI to be compiled before running Cypress
printf "Waiting for GUI to compile"
until $(curl --output /dev/null --silent --head --fail http://ace2-ams:8080); do
    printf "."
    sleep 1
done

# Run Cypress
docker exec ace2-ams-gui xvfb-run cypress run --headed --browser chrome --config video=false,screenshotOnRunFailure=false