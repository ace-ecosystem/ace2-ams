#!/usr/bin/env bash

cd db_api/app
black .

cd ..

cd gui_api/app
black .