#!/bin/bash

# get path to module without trailing slashes
path=$(echo $1 | sed 's:/*$::')

# create image name from module path basename
name=${path##*/}

# build module image
docker build --build-arg module=$path -t analysis-module-$name -f aws/Dockerfile.analysis_module .
