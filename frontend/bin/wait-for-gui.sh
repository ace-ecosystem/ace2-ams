#!/usr/bin/env bash

printf "Waiting for the API to be accessible"
i=0
until $(curl --output /dev/null --silent --fail http://ace2-ams:8080/api/ping); do
    printf "."
    ((i=i+1))

    if [ $i -gt 60 ]
    then
        printf "Something went wrong! Check the API logs!\n"
        exit 1
    fi

    sleep 1
done

printf "\n"

printf "Waiting for the GUI to be accessible"
i=0
until $(curl --output /dev/null --silent --fail http://ace2-ams:8080/login); do
    printf "."
    ((i=i+1))

    if [ $i -gt 60 ]
    then
        printf "Something went wrong! Check the GUI logs!\n"
        exit 1
    fi

    sleep 1
done
