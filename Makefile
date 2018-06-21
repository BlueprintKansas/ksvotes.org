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
	python manage.py runserver 2> testserver.log &

stop-testserver:
	kill -9 `cat server.pid` && rm server.pid

livetest:
	bin/live-test.sh

locales:
	bin/build-locales

translate:
	venv/bin/pybabel compile -d app/translations
	bin/pop-translate.pl translations.csv

build: translate

.PHONY: deps venv test dbmigrate run testcov
