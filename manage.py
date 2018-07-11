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
    import csv
    with open('county-clerks.csv', newline="\n") as csvfile:
        next(csvfile)  # skip headers
        # GEOCODE_FORMAT,COUNTY,OFFICER,EMAIL,HOURS,PHONE,FAX,ADDRESS1,ADDRESS2,CITY,STATE,ZIP
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            ucfirst_county = row[1][0] + row[1][1:].lower()
            clerk = Clerk.find_or_create_by(county=ucfirst_county)
            clerk.officer = row[2]
            clerk.email = row[3]
            clerk.phone = row[5]
            clerk.fax = row[6]
            clerk.address1 = row[7]
            clerk.address2 = row[8]
            clerk.city = row[9]
            clerk.state = row[10]
            clerk.zip = row[11]
            clerk.save(db.session)


if __name__ == "__main__":
    write_pid_file()
    manager.run()
