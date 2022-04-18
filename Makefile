check:
	@[ -f ".env" ] || (echo "Missing .env file" && false)
	@python manage.py check_configuration

deps:
	pip install -r requirements.txt
	rm -f package-lock.json && yarn install

venv:
	@echo 'You must run: . venv/bin/activate'

crypt-key:
	python manage.py generate_crypt_key

demo-uuid:
	python manage.py generate_demo_uuid

dbmigrate:
	python manage.py db migrate

dbupgrade:
	python manage.py db upgrade

update: dbmigrate dbupgrade

migrate: dbupgrade

db:
	@psql `grep ^DATABASE_URL= .env | sed -e "s/DATABASE_URL=//"`

shell:
	python manage.py shell

run:
	python manage.py runserver -h 0.0.0.0

testcov:
	py.test --cov-report term-missing --cov --ignore=node_modules

test: check
	py.test -s -vv app/

jstest:
	behave

css:
	npm run css

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

redact:
	python manage.py redact_pii

export:
	python manage.py export_registrants

start-services:
	docker-compose up -d

stop-services:
	docker-compose down

DOCKER_IMG="ksvotes:flask-web"
DOCKER_NAME="ksvotes-flask-web"
ifeq (, $(shell which docker))
DOCKER_CONTAINER_ID := docker-is-not-installed
else
DOCKER_CONTAINER_ID := $(shell docker ps --filter ancestor=$(DOCKER_IMG) --format "{{.ID}}" -a)
endif

container-build:
	docker build -f Dockerfile -t $(DOCKER_IMG) .

container-run:
	docker run -p 8081:8081 -it $(DOCKER_IMG)

login:
	docker run --rm -it --name $(DOCKER_NAME) \
	--add-host=host.docker.internal:host-gateway \
	--network ksvotesorg_app-tier \
	-v $(PWD):/app -p 5000:5000 $(DOCKER_IMG) /bin/bash

CI_OPTS=-f docker-compose.yml -f docker-compose-ci.yml --env-file=.env-ci

ci-build:
	ENV_NAME=ci docker-compose $(CI_OPTS) build

ci-start:
	ENV_NAME=ci docker-compose $(CI_OPTS) up -d --no-recreate

ci-stop:
	ENV_NAME=ci docker-compose $(CI_OPTS) down

ci-test:
	ENV_NAME=ci docker-compose $(CI_OPTS) logs --tail="all"
	ENV_NAME=ci docker exec web ./run-ci-tests.sh

ci-clean:
	ENV_NAME=ci docker-compose $(CI_OPTS) down --rmi all


.PHONY: deps venv test dbmigrate run testcov fixtures redact export start-services stop-services
