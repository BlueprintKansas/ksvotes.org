web: newrelic-admin run-program gunicorn manage:app --max-requests 500 --preload 
release: make dbupgrade load-clerks load-zipcodes
