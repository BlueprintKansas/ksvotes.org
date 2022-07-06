# KSVotes.org

[![Build Status](https://github.com/BlueprintKansas/ksvotes.org/actions/workflows/pull_request.yml/badge.svg)](https://github.com/BlueprintKansas/ksvotes.org)

The ksvotes.org site makes Kansas online voting registration easy.

## Table of Contents
* [Database Setup](#database-setup)
* [Setup & Installation](#setup-&-installation)
    * [Environmental Variables](#environmental-variables)
    * [Migrate Database](#migrate-database)
    * [Run the application](#run-the-application)
* [Tests](#tests)
* [Styling](styling)
* [Internationalization & Localization](#internationalization-&-localization)

### Database services

You run PostgreSQL and Redis via Docker.

See the `docker-compose.yml` file in the repo. You can use with:

```
$ make services-start
$ make services-stop
```

Redis is used for caching stats and external API calls.

Once you have PostgreSQL available, you must create database instances for local use.
[DB setup reference](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e)

Create databases for development and testing. In the [Environmental Variables](#environmental-variables)
section below we assume the names you picked were `ksvotes_dev` and `ksvotes_test`.


## Setup & Installation
Recommendations for running after cloning:

Install [Python 3.10+](https://www.python.org/downloads/)

Install [pip](https://pypi.org/project/pip/#description)

Install [virtualenv](https://virtualenv.pypa.io/en/stable/)

In app root directory setup your virtualenv and install dependencies to your virtualenv python.

```
$ python3 -m venv venv
$ . venv/bin/activate
$(venv) make deps
$(venv) make locales
```

## /etc/hosts file

You'll want to add some entries to your local `/etc/hosts` file to make using Docker easier.

```
127.0.0.1  ksvotes-postgres
127.0.0.1  redis
127.0.0.1  test.ksvotes.org
```

## Create databases

```sh
$(venv) PGPASSWORD=postgres psql -c 'create database "ksvotes.org_test";' -U postgres -h ksvotes-postgres
$(venv) PGPASSWORD=postgres psql -c 'create database "ksvotes.org_dev";' -U postgres -h ksvotes-postgres
$(venv) psql -c "create user foo with password 'bar';" -U postgres -h ksvotes-postgres
```

### Environmental Variables
Create a .env file in the root directory and add the following variables.
Note that the commented-out (`#`-prefixed) variables are optional.

```
DATABASE_URL=postgresql://foo:bar@ksvotes-postgres/ksvotes_dev
TESTING_DATABASE_URL=postgresql://foo:bar@ksvotes-postgres/ksvotes_test
SECRET_KEY={{generate a secret key}}
APP_CONFIG=development
CRYPT_KEY={{generate a secret key | base64}}

# Set this to enable the /demo endpoint
DEMO_UUID={{generate a UUID and run "make load-demo"}}

# You can grab one from the URL below or take the one from the staging configuration
USPS_USER_ID={{key from https://registration.shippingapis.com/}}

#########################
# OPTIONAL ENV VARS
#########################

# LOG_LEVEL=INFO
# GA_KEY={{google analytics key}}
# RECAPTCHA_KEY={{public key}}
# RECAPTCHA_SECRET={{private key}}
# AWS_ACCESS_KEY_ID={{from role with at least rds access}}
# AWS_SECRET_ACCESS_KEY={{from role with at least rds access}}
# AWS_DEFAULT_REGION={{us-east-1 || or your region where RDS is hosted}}
# SES_ACCESS_KEY_ID={{from role with ses access}}
# SES_SECRET_ACCESS_KEY={{from role with ses access}}

# TEST_CLERK_EMAIL={{override the Clerk.email value for the TEST County}}
# EMAIL_FROM={{override the From email header in all email}}
# EMAIL_PREFIX={{prefix all Subject lines with a string}}

# Default is not to send actual email unless SEND_EMAIL is set
# SEND_EMAIL=true

# Number of minutes before idle session expires. Default is 10.
# SESSION_TTL=10

# You want the default VV URL unless you are testing error checking.
# VOTER_VIEW_URL=https://myvoteinfo.voteks.org/VoterView/RegistrantSearch.do


# The date and time prior to the Primary election when the Advance Ballot
# option for the Primary disappears. Format is 'YYYY-MM-DD HH:MM:SS' and assumes
# a Central US time zone
# AB_PRIMARY_DEADLINE="2020-05-01 17:00:00"

# Turn the AB flow on. Default is off.
# ENABLE_AB=true

# Turn VIT voting location JS widget on. Default is off.
# ENABLE_VOTING_LOCATION=true

# Turn off HTTPS requirement. Probably set this to true in your local dev.
# SSL_DISABLE=true

# Turn on lots of SQL debugging.
# SQL_DEBUG=true

# Include the top banner on every page that this is not the live production site.
# STAGE_BANNER=true

# Airtable is managed by ksvoterguide.org folks for early voting and ballot dropbox locations.
# AIRTABLE_EV_KEY=sekrit
# AIRTABLE_EV_BASE_ID=sekrit
# to temporarily disable, leave the table names commented out
# AIRTABLE_EV_TABLE='SoS 10-19-2020'
# AIRTABLE_DROPBOX_TABLE='dropbox 2020'
```

### Crypt Key

The encryption key is kind of particular, it needs to be 32 bytes long and URl-safe base64 encoded.  Use this command to generate one for you using the cryptography library:

```
$(venv) make crypt-key
```

### Demo uuid

We need `DEMO_UUID` set to a UUID, use this to generate one for you quickly:

```
$(venv) make demo-uuid
```

### Validate your configuration

You can check that your local env has all of the requried environment variables set by running:

```
($venv) make check
```

### Migrate Database
Once setup is complete let's get our models imported into our development database.

```
$(venv) make dbupgrade
```

When you modify the model classes and want to apply to the schema:

```
$(venv) make update
```

### Run the Application

Let's get up and running.

First, build the container image:

```sh
$(venv) make container-build
```

Second, login to the container:

```sh
$(venv) make login
```

If you get an error like `docker: Error response from daemon: network ksvotesorg_app-tier not found.` make sure you have the redis/postgresql services running
with `make services-stop`.

Third, start the app:

```sh
ksvotesapp@randomstr:/app$ make run
```

Navigate to [test.ksvotes.org:5000](http://test.ksvotes.org:5000)


## Tests

To run all unit tests (inside the Docker container):

```sh
ksvotesapp@randomstr:/app$ make test
```

To run all unit tests with coverage:

```sh
ksvotesapp@randomstr:/app$ make testcov
```

### Browser tests

Run browser-based tests outside the container, on your native host:

```sh
$(venv) make playwright
```

## Styling

Code is currently setup to SCSS with node scripts to compile.

Edit `scss/source.scss` and compile with `% make css`.

Alternatively you can create your own .css style sheet in *app/static/css* and replace

```html
<link href="{{url_for('static', filename='css/compiled.css')}}" rel="stylesheet">
```

in *app/templates/base.html* with

```html
<link href="{{url_for('static', filename='css/[[[name of your style sheet]]]')}}" rel="stylesheet">
```

To setup scss watcher in root directory run:

```sh
$ npm install
$ npm run watch
```

## Internationalization & Localization
This application is using [Flask-Babel](https://pythonhosted.org/Flask-Babel/)

To add a new string, reference the string in the .py code with `gettext()` or `lazy_gettext()`
and then run `% make locales` to update the corresponding babel files. For example:

```
# in foo.py
lazy_gettext('some_key_string')

# add 'some_key_string' to translations.json
% vi translations.json

# Then in your terminal
# update the translation files
% make locales
```

