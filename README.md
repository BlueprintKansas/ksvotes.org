# KSVotes.org
**Note: This is repo is in active development.  Not recommended to pull and run at this point**

[![Build Status](https://travis-ci.org/BlueprintKansas/ksvotes.org.svg?branch=master)](https://travis-ci.org/BlueprintKansas/ksvotes.org)

The ksvotes.org site makes Kansas online voting registration easy.

## Table of Contents
* [Setup & Installation](#setup-&-installation)
    * [Database Setup](#database-setup)
    * [Environmental Variables](#environmental-variables)
    * [Migrate Database](#migrate-database)
    * [Run the application](#run-the-application)
* [Tests](#tests)
* [Styling](styling)
* [Internationalization & Localization](#internationalization-&-localization)

## Setup & Installation
  Recommendations for running after cloning:

  Install [Python 3.6+](https://www.python.org/downloads/)

  Install [pip](https://pypi.org/project/pip/#description)

  Install [virtualenv](https://virtualenv.pypa.io/en/stable/)

  In app root directory setup your virtualenv and install dependencies to your virtualenv python.

  ```
  $ virtualenv venv -p python3
  ```
  ```
  $ . venv/bin/activate
  ```
  ```
  $(venv) pip install -r requirements.txt
  ```

### Database Setup
  For Mac installations I like [PostgresApp](https://postgresapp.com/)

  [DB setup reference](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e)

  Setup a development postgres database.

  Setup a testing postgres database.

### Environmental Variables
  Create a .env file in the root directory and add the following variables.
  ```
  DATABASE_URL={{your development database connection string}}
  TESTING_DATABASE_URL={{your testing database connection string}}
  SECRET_KEY={{generate a secret key}}
  APP_CONFIG=development
  LOG_LEVEL=INFO
  NAV=true
  CRYPT_KEY={{generate a secret key | base64}}
  GA_KEY={{google analytics key}}
  # RECAPTCHA_KEY={{public key}}
  # RECAPTCHA_SECRET={{private key}}
  # USPS_USER_ID={{key from https://registration.shippingapis.com/}}
  # AWS_ACCESS_KEY_ID={{from role with at least rds and an ses access}}
  # AWS_SECRET_ACCESS_KEY={{from role with at least rds and an ses access}}
  # AWS_DEFAULT_REGION={{us-east-1 || or your region where RDS is hosted}}
  # NVRIS_URL={{https://full-url-to-nvris-instance-no-trailing-slash.com}}
  ```

### Migrate Database
  Once setup is complete let's get our models imported into our development database.

  Note: init command should only be run once per database and does not need to be run on the testing database.  After that if you make changes to the database models you will need to run the migrate and upgrade commands for your dev and production databases.

  ```
  $(venv) python manage.py db init
  ```

  ```
  $(venv) python manage.py db migrate
  ```

  ```
  $(venv) python manage.py db upgrade
  ```


### Run the Application
  Let's get up and running.
  ```
  $(venv) python manage.py runserver
  ```

  Navigate to [127.0.0.1:5000](127.0.0.1:5000)



## Tests
To run all tests with coverage:
```
$(venv) py.test --cov-report term-missing --cov --ignore=node_modules
```


## Styling
Code is currently setup to SCSS with node scripts to compile.

Edit `scss/source.scss` and compile with `% make css`.

Alternatively you can create your own .css style sheet in *app/static/css* and replace
```
<link href="{{url_for('static', filename='css/compiled.css')}}" rel="stylesheet">
```
in *app/templates/base.html* with
```
<link href="{{url_for('static', filename='css/[[[name of your style sheet]]]')}}" rel="stylesheet">
```

To setup scss watcher in root directory run:
```
$ npm install
```
```
$ npm run watch
```

## Internationalization & Localization
This application is using [Flask-Babel](https://pythonhosted.org/Flask-Babel/)

To add a new string, reference the string in the .py code with `gettext()` or `lazy_gettext()`
and then run `% make locales` to update the corresponding babel files. For example:

```
# in foo.py
lazy_gettext('some_key_string')

# add 'some_key_string' to translations.csv
% vi translations.csv

# Then in your terminal
# update the translation files
% make locales
```

