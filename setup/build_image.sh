#!/bin/bash

# bail on any error
set -e

# get optional args
env="prod"
while getopts "e:" flag; do
case "$flag" in
    e) env=$OPTARG;;
esac
done

# suppress scan suggestions
export DOCKER_SCAN_SUGGEST=false

# get path without trailing slashes
path=$(echo ${@:$OPTIND:1} | sed 's:/*$::')

# get image type from path
type=${path%/*}

# get image name from path
name=${path##*/}
name=$(echo $name | awk '{print tolower($0)}')

# build image base
if [ -f "$path/Dockerfile" ]; then
    docker build -t ace2-$type-$name-base -f $path/Dockerfile .
else
    docker build -t ace2-$type-$name-base -f setup/ace2-base.Dockerfile .
fi

# build image
docker build \
    --build-arg name=$name \
    --build-arg env=$env \
    -t ace2-$type-$name \
    -f setup/ace2-$type.Dockerfile \
    .
