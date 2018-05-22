deps:
	pip install -r requirements.txt

venv:
	virtualenv venv -p python3

dbmigrate:
	python manage.py db migrate
	python manage.py db upgrade

run:
	python manage.py runserver

test:
	echo 'testing is TODO'

.PHONY: deps venv test dbmigrate run
