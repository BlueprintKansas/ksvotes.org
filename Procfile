web: newrelic-admin run-program gunicorn manage:app --max-requests 500 --preload --timeout 12
release: make dbupgrade load-clerks load-zipcodes
