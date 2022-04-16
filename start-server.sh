#!/bin/sh

set -e

make dbupgrade load-clerks load-zipcodes
gunicorn --bind 0.0.0.0:$PORT manage:app --max-requests 500 --preload
