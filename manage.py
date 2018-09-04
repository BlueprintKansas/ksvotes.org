import os
import signal

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
    regs = Registrant.query.all()
    exporter = RegistrantExporter(regs)
    exporter.export()


if __name__ == "__main__":
    write_pid_file()
    manager.run()
