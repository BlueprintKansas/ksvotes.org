help: ## Print the help documentation
	@grep -E '^[/a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

check: ## Check your .env file
	@[ -f ".env" ] || (echo "Missing .env file" && false)
	@python manage.py check_configuration

deps: ## Install dependencies
	pip install -U -r requirements.txt
	pip install -U -r requirements-ci.txt
	npm install
	playwright install

venv:
	@echo 'You must run: . venv/bin/activate'

crypt-key: ## Generate a CRYPT_KEY value
	python manage.py generate_crypt_key

demo-uuid: ## Generate a UUID
	python manage.py generate_demo_uuid

dbmigrate: ## Generate db migrations
	python manage.py db migrate

dbupgrade: ## Perform db migrations
	python manage.py db upgrade

update: dbmigrate dbupgrade

migrate: dbupgrade ## Alias for dbupgrade

db: ## Connect to db via psql
	@psql `grep ^DATABASE_URL= .env | sed -e "s/DATABASE_URL=//"`

shell: ## Open interactive Flask shell
	python manage.py shell

run: ## Run the dev server
	python manage.py runserver -h 0.0.0.0

testcov: ## Run unit tests with coverage report
	py.test --cov-report term-missing --cov --ignore=node_modules --cov-fail-under 90

test: check ## Run unit tests
	py.test -s -vv app/

jstest: ## Run behave tests
	behave

playwright: ## Run playwrite tests
	pytest -s -vv --base-url=http://test.ksvotes.org:5000 playwright/

css: ## Build css artifacts from scss
	npm run css

locales: ## Build the i18n translation files
	bin/build-locales

build: locales

routes: ## List available routes
	python manage.py list_routes

load-clerks: ## Load clerks into db from .csv file
	python manage.py load_clerks

load-demo: ## Load the demo registrant
	python manage.py load_demo

load-zipcodes: ## Load the ZIP Codes into db from .csv file
	python manage.py load_zipcodes

fixtures: load-clerks load-demo load-zipcodes ## Load all .csv file data

deploy-stage-fixtures: ## Make fixtures in the ksvotes-staging env
	heroku run 'make fixtures' --app ksvotes-staging

deploy-prod-fixtures: ## Make fixtures in the ksvotes-production env
	heroku run 'make fixtures' --app ksvotes-production

redact: ## Remove PII from the encrypted db column(s)
	python manage.py redact_pii

export: ## Generate .csv output from db
	python manage.py export_registrants

services-start: ## Start Redis+PostgreSQL locally
	docker-compose up -d

start-services: services-start ## Alias for services-start

services-stop: ## Stop Redis+PostgreSQL locally
	docker-compose down

stop-services: services-stop ## Alias for services-stop

DOCKER_IMG=ksvotes:flask-web
DOCKER_NAME=ksvotes-flask-web
ifeq (, $(shell which docker))
DOCKER_CONTAINER_ID := docker-is-not-installed
else
DOCKER_CONTAINER_ID := $(shell docker ps --filter ancestor=$(DOCKER_IMG) --format "{{.ID}}" -a)
DOCKER_CONTAINER_ID_CI := $(shell docker ps --filter ancestor=ksvotes:ci --format "{{.ID}}" -a)
endif

container-build: ## Build the app docker image
	docker build -f Dockerfile -t $(DOCKER_IMG) --build-arg GIT_SHA=`git rev-parse HEAD | cut -c1-8` .

container-run: ## Run the app docker image
	docker run -p 8081:8081 -it $(DOCKER_IMG)

login: ## Open a shell on the local app docker image
	docker run --rm -it --name $(DOCKER_NAME) \
	--add-host=host.docker.internal:host-gateway \
	--network ksvotesorg_app-tier \
	-v $(PWD):/app -p 5000:5000 $(DOCKER_IMG) /bin/bash

CI_OPTS=-f docker-compose.yml -f docker-compose-ci.yml --env-file=.env-ci

ci-build: ## Build docker images in CI
	docker build -f Dockerfile -t $(DOCKER_IMG)-ci --build-arg ENV_NAME=ci .
	ENV_NAME=ci docker-compose $(CI_OPTS) build

ci-start: ci-build ## Start the docker-compose services in CI
	ENV_NAME=ci docker-compose $(CI_OPTS) up -d --no-recreate

ci-stop: ## Stop the docker-compose services in CI
	ENV_NAME=ci docker-compose $(CI_OPTS) down

ci-test: ci-logs ## Run the unit tests in CI
	ENV_NAME=ci docker exec web ./run-ci-tests.sh

ci-clean: ## Remove the docker images in CI
	ENV_NAME=ci docker-compose $(CI_OPTS) down --rmi all

ci-logs: ## Tail the docker-compose logs for CI
	ENV_NAME=ci docker-compose $(CI_OPTS) logs --tail="all"

ci-logs-tail: ## Tail -f the docker-compose logs for CI
	ENV_NAME=ci docker-compose $(CI_OPTS) logs -f

ci-attach: ## Attach to a running container and open a shell (like login for running container)
	docker exec -it $(DOCKER_CONTAINER_ID_CI) /bin/bash



.PHONY: deps venv test dbmigrate run testcov fixtures redact export start-services stop-services playwright
