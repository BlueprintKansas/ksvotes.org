check:
	@[ -f ".env" ] || (echo "Missing .env file" && false)

deps:
	pip install -r requirements.txt

venv:
	virtualenv venv -p python3

dbmigrate:
	python manage.py db migrate

dbupgrade:
	python manage.py db upgrade

update: dbmigrate dbupgrade

run:
	python manage.py runserver

testcov:
	py.test --cov-report term-missing --cov

test: check
	py.test

.PHONY: deps venv test dbmigrate run testcov
