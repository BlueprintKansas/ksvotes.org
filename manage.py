import os

from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import url_for

app = create_app(os.getenv('APP_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


def write_pid_file():
    pid = str(os.getpid())
    with open('server.pid', 'w+') as f:
        f.write(pid + '\n')


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def load_clerks():
    Clerk.load_fixtures()


@manager.command
def load_demo():
    Registrant.load_fixtures()


@manager.command
def load_zipcodes():
    ZIPCode.load_fixtures()


@manager.command
def redact_pii():
    from datetime import datetime, timedelta
    days_ago = timedelta(days=int(os.getenv('REDACT_OLDER_THAN_DAYS', 2)))
    Registrant.redact_pii(datetime.utcnow() - days_ago)


@manager.command
def export_registrants():
    from app.services.registrant_exporter import RegistrantExporter
    if os.getenv('SINCE'):
      regs = Registrant.query.filter(Registrant.updated_at > os.getenv('SINCE')).yield_per(200).enable_eagerloads(False)
    else:
      regs = Registrant.query.yield_per(200).enable_eagerloads(False)

    exporter = RegistrantExporter(regs)
    exporter.export()


@manager.command
def generate_crypt_key():
    """ Generate a new valid CRYPT_KEY """
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    print("\nAdd this to your .env file:")
    print('CRYPT_KEY="{}"'.format(key.decode('ascii')))


@manager.command
def generate_demo_uuid():
    import uuid
    this_uuid = uuid.uuid4().hex

    print("\nAdd this to your .env file:")
    print('DEMO_UUID="{}"'.format(this_uuid))


@manager.command
def check_configuration():
    """ Ensure our configuration looks plausible """
    required_env_settings = [
        'DATABASE_URL',
        'TESTING_DATABASE_URL',
        'SECRET_KEY',
        'APP_CONFIG',
        'CRYPT_KEY',
        'NVRIS_URL',
        'DEMO_UUID',
        'USPS_USER_ID',
    ]
    missing = []

    for key in required_env_settings:
        value = os.getenv(key, None)
        if value is None or value.startswith('{'):
            missing.append(key)

    if missing:
        print("Configuration Errors Detected, these are missing:")
        [print(k) for k in missing]


if __name__ == "__main__":
    write_pid_file()
    manager.run()
