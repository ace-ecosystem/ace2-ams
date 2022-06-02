#!/bin/bash

# get current branch
branch=`git rev-parse --abbrev-ref HEAD`
echo $branch

# fetch all changes from remotes
git fetch --all

# checkout a new branch based on origin master
git checkout -B publish/master -t origin/master

# remove private files
find . -name '*.private*' -exec git rm -r --ignore-unmatch {} +
git commit -m 'removed private files'

# squash merge publish/master into branch of upstream/main and push it out
git checkout -B publish/main -t upstream/main
git merge --squash -X ours publish/master
git commit -m '$1'
git push upstream HEAD

# cleanup branches
git checkout $branch
git branch -D publish/master
git branch -D publish/main
