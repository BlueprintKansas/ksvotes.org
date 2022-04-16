make dbupgrade load-clerks load-zipcodes
gunicorn manage:app --max-requests 500 --preload
