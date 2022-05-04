#!/bin/bash

set -e
set -x

# make sure .env exists (at Heroku it will not)
touch .env
export $(cat .env | grep -v ^# | xargs)

if [ "${ENV_NAME}" == "ci" ]; then
  set +e
  psql -c "drop database ksvotes_test;" -U postgres -h ksvotes-postgres
  psql -c "drop user foo;" -U postgres -h ksvotes-postgres
  set -e
  psql -c "create database ksvotes_test;" -U postgres -h ksvotes-postgres
  psql -c "CREATE USER foo WITH PASSWORD 'bar';" -U postgres -h ksvotes-postgres
fi

make dbupgrade load-clerks load-zipcodes

newrelic-admin run-program gunicorn --bind 0.0.0.0:${PORT:=5000} manage:app --max-requests 1000 --preload --access-logfile -
