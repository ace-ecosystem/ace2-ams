#!/bin/bash

# get path to lib without trailing slashes
path=$(echo $1 | sed 's:/*$::')

# get lib name from path basename
name=${path##*/}
name=$(echo $name | awk '{print tolower($0)}')

# build lib base image
docker build -t ace2-lib-$name-base -f $path/Dockerfile .

# build lib image
docker build --build-arg lib=$path --build-arg name=$name -t ace2-lib-$name -f setup/ace2-lib.Dockerfile .
