web: newrelic-admin run-program gunicorn manage:app --max-requests 500 --preload 0.0.0.0:$PORT
release: make dbupgrade load-clerks load-zipcodes
