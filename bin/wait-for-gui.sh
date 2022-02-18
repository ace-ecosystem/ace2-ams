#!/usr/bin/env bash

printf "Waiting for the API to be accessible"
until $(curl --output /dev/null --silent --fail http://ace2-ams:8080/api/ping); do
    printf "."
    sleep 1
done

printf "\n"

printf "Waiting for the GUI to be accessible"
until $(curl --output /dev/null --silent --fail http://ace2-ams:8080/login); do
    printf "."
    sleep 1
done