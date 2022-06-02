#!/bin/bash

# get path to module without trailing slashes
path=$(echo $1 | sed 's:/*$::')

# create image name from lowercased module path basename
name=${path##*/}
name=$(echo $name | awk '{print tolower($0)}')

# build module image
docker build --build-arg module=$path -t ace2-module-$name -f setup/aws/Dockerfile-ace2-module .
