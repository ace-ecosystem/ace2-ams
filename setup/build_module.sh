#!/bin/bash

# get path to module without trailing slashes
path=$(echo $1 | sed 's:/*$::')

# create image name from lowercased module path basename
name=${path##*/}
name=$(echo $name | awk '{print tolower($0)}')

# build module base image
docker build -t ace2-module-$name-base -f $path/Dockerfile .

# build module image
docker build --build-arg module=$path --build-arg name=$name -t ace2-module-$name -f setup/ace2-module.Dockerfile .
