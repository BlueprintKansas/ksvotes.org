check:
	@[ -f ".env" ] || (echo "Missing .env file" && false)

deps:
	pip install -r requirements.txt
	npm install

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
	py.test -s app/

jstest:
	npm run test

start-testserver:
ifeq ($(DEBUG), zombie)
	python manage.py runserver &
else
	python manage.py runserver &> testserver.log &
endif

stop-testserver:
	kill -9 `cat server.pid` && rm server.pid

livetest:
	bin/live-test.sh

locales:
	bin/build-locales

build: locales

.PHONY: deps venv test dbmigrate run testcov
