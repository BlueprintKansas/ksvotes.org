check:
	@[ -f ".env" ] || echo "Missing .env file"

deps:
	pip install -r requirements.txt

venv:
	virtualenv venv -p python3

dbmigrate:
	python manage.py db migrate
	python manage.py db upgrade

run:
	python manage.py runserver

testcov:
	py.test --cov-report term-missing --cov

test: check
	py.test

.PHONY: deps venv test dbmigrate run testcov
