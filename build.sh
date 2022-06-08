#!/bin/bash

# build base
docker build -t ace2-base -f setup/aws/ace2-base.Dockerfile .

# build ace lib
docker build -t ace2-lib-ace2 -f setup/aws/ace2-lib-ace2.Dockerfile .

# TODO: build all other libs
for d in lib/*/ ; do
    echo "$d"
done

# build all modules
for d in modules/*/ ; do
    # get path to module without trailing slashes
    path=$(echo $d | sed 's:/*$::')

    # create image name from lowercased module path basename
    name=${path##*/}
    name=$(echo $name | awk '{print tolower($0)}')

    # build image with mod deps
    docker build -t ace2-module-$name-base -f $path/Dockerfile .

    # build the module
    docker build --build-arg module=$path --build-arg name=$name -t ace2-module-$name -f setup/aws/ace2-module.Dockerfile .
done
