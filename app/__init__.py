import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from config import config, LANGUAGES
import logging
from flask.logging import default_handler

db = SQLAlchemy()
babel = Babel()

def create_app(config_name):
    os.environ["FLASK_ENV"] = config_name
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    babel.init_app(app)

    # logging config
    app.logger.setLevel(os.getenv('LOG_LEVEL', default='WARN'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    default_handler.setFormatter(formatter)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(LANGUAGES.keys())
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
