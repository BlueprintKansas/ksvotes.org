# KSVotes.org

[![Build Status](https://travis-ci.com/BlueprintKansas/ksvotes.org.svg?branch=master)](https://travis-ci.com/BlueprintKansas/ksvotes.org)

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

### Database Setup
  For Mac installations I like [PostgresApp](https://postgresapp.com/)

  [DB setup reference](https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e)

  Create databases for development and testing. In the [Environmental Variables](#environmental-variables) section below we assume the names you picked were `ksvotes_dev` and `ksvotes_test`.


## Setup & Installation
  Recommendations for running after cloning:

  Install [Python 3.6+](https://www.python.org/downloads/)

  Install [pip](https://pypi.org/project/pip/#description)

  Install [virtualenv](https://virtualenv.pypa.io/en/stable/)

  In app root directory setup your virtualenv and install dependencies to your virtualenv python.

  ```
  $ virtualenv venv -p python3
  $ . venv/bin/activate
  $(venv) make deps
  $(venv) make locales
  ```

### Environmental Variables
  Create a .env file in the root directory and add the following variables.
  ```
  DATABASE_URL=postgres://localhost/ksvotes_dev
  TESTING_DATABASE_URL=postgres://localhost/ksvotes_test
  SECRET_KEY={{generate a secret key}}
  APP_CONFIG=development
  LOG_LEVEL=INFO
  CRYPT_KEY={{generate a secret key | base64}}
  GA_KEY={{google analytics key}}
  # RECAPTCHA_KEY={{public key}}
  # RECAPTCHA_SECRET={{private key}}
  # USPS_USER_ID={{key from https://registration.shippingapis.com/}}
  # AWS_ACCESS_KEY_ID={{from role with at least rds access}}
  # AWS_SECRET_ACCESS_KEY={{from role with at least rds access}}
  # AWS_DEFAULT_REGION={{us-east-1 || or your region where RDS is hosted}}
  # SES_ACCESS_KEY_ID={{from role with ses access}}
  # SES_SECRET_ACCESS_KEY={{from role with ses access}}
  # NVRIS_URL={{https://full-url-to-nvris-instance-no-trailing-slash.com}}
  # TEST_CLERK_EMAIL={{override the Clerk.email value for the TEST County}}
  # EMAIL_FROM={{override the From email header in all email}}
  # Default is not to send actual email unless SEND_EMAIL is set
  # SEND_EMAIL=true
  # Number of minutes before idle session expires. Default is 10.
  SESSION_TTL=10
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
  ```
  $(venv) make run
  ```

  Navigate to [127.0.0.1:5000](127.0.0.1:5000)



## Tests
To run all tests with coverage:
```
$(venv) make testcov
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

# add 'some_key_string' to translations.json
% vi translations.json

# Then in your terminal
# update the translation files
% make locales
```

