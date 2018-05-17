# KSVotes.org
**Note: This is repo is in active development.  Not recommended to pull and run at this point**

The ksvotes.org site makes Kansas online voting registration easy.

## Table of Contents
* [Setup & Installation](#setup-&-installation)
    * [Database Setup](#database-setup)
    * [Environmental Variables](#environmental-variables)
    * [Migrate Database](#migrate-database)
    * [Run the application](#run-the-application)

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
APP_CONFIG=dev
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

Navigate to 127.0.0.1:5000