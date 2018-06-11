import os
import signal

from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

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

if __name__ == "__main__":
    write_pid_file()
    manager.run()
