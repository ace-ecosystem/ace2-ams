#!/usr/bin/env bash

cd frontend
npx prettier --write .
eslint . --fix