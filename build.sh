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

# build ace2 base
docker build --target ace2-base -t ace2-base -f Dockerfile .

# build ace2
docker build --build-arg env=$env -t ace2 -f Dockerfile .

function build_image() {
    # get path without trailing slashes
    path=$(echo $1 | sed 's:/*$::')

    # get image type from path
    type=${path%/*}

    # get image name from path
    name=${path##*/}

    # skip empty directory
    if [ "$name" = "*" ] ; then
        return
    fi

    # build image base
    if [ -f "$path/Dockerfile" ]; then
        docker build -t ace2-$type-$name-base -f $path/Dockerfile .
    else
        docker build --target ace2-base -t ace2-$type-$name-base -f Dockerfile .
    fi

    # build image
    docker build --build-arg name=$name --build-arg env=$env -t ace2-$type-$name -f $type/Dockerfile .
}

# build all modules
for path in services/*/ ; do
    build_image $path
done
