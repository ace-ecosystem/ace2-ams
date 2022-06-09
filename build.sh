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

# build base
docker build -t ace2-base -f setup/ace2-base.Dockerfile .

# build the ace2 lib first
setup/build_image.sh -e $env lib/ace2/

# build all other libs
for lib in lib/*/ ; do
    # skip the ace2 lib
    if [ "$lib" = "lib/ace2/" ]; then
        continue
    fi

    setup/build_image.sh -e $env $lib
done

# build all modules
for module in modules/*/ ; do
    setup/build_image.sh -e $env $module
done
