#!/usr/bin/env bash

# Sleep until the web application is actually ready
until $(curl --output /dev/null --silent --fail "http://ace2-ams:8080/login"); do
    sleep 1
done

# Run the tests
cypress run --headless --config video=false,screenshotOnRunFailure=false