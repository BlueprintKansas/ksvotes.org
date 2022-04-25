#!/bin/bash

# exit if any command fails
set -e
set -x

wait-for-it -t 60 ksvotes-postgres:5432
wait-for-it -t 60 127.0.0.1:5000

export $(cat .env | grep -v ^# | xargs)
env

make test
