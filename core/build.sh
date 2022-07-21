#!/bin/bash

# bail on any error
set -e

usage() {
    echo "Builds ACE2 service images"
    echo ""
    echo "Usage: $0 [<options>] dir ..."
    echo ""
    echo "Args:"
    echo "    dir          list of service directories to build images for"
    echo "                 if no directories are given then build all images"
    echo ""
    exit
}

# get optional args
while getopts h: flag; do
case "$flag" in
    h) usage;;
    ?) usage;;
esac
done

# suppress scan suggestions
export DOCKER_SCAN_SUGGEST=false

# build all services by default
services=${@:$OPTIND}
if [ "$services" = "" ]; then
    services="services/*/"
fi

## build all modules
for path in $services ; do
    # get path without trailing slashes
    path=$(echo $path | sed 's:/*$::')

    # get image type from path
    type=${path%/*}

    # get image name from path
    name=${path##*/}

    # skip empty directory
    if [ "$name" = "*" ] ; then
        return
    fi

    # merge service dockerfile commands into Dockerfile and build the image
    while read -r line; do 
        if [[ "$line" == "DEPENDENCIES" ]]; then 
            if [ -f "$path/Dockerfile" ]; then
                cat $path/Dockerfile
            fi
        else
            echo "$line"
        fi
    done < Dockerfile | docker build --build-arg name=$name -t $name -f - .
done

# remove dangling images
docker image prune -f
