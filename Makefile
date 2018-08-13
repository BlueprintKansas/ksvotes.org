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

db:
	psql -h localhost ksvotes_dev

shell:
	python manage.py shell

run:
	python manage.py runserver

testcov:
	py.test --cov-report term-missing --cov --ignore=node_modules

test: check
	py.test -s app/

jstest:
	npm run test

css:
	npm run css

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

routes:
	python manage.py list_routes

load-clerks:
	python manage.py load_clerks

load-demo:
	python manage.py load_demo

load-zipcodes:
	python manage.py load_zipcodes

fixtures: load-clerks load-demo load-zipcodes

deploy-prod:
	git push production master

deploy-stage-fixtures:
	heroku run 'make fixtures' --app ksvotes-staging

deploy-prod-fixtures:
	heroku run 'make fixtures' --app ksvotes-production

.PHONY: deps venv test dbmigrate run testcov fixtures
