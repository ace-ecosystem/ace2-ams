#!/usr/bin/env bash

matches="$(grep -R '\.only(' frontend/tests)"
if [ -z "$matches" ]
then
    exit 0
else
    echo "$matches"
    exit 1
fi