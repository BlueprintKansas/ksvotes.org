import os
from flask import Flask, request, g, abort
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from config import config, LANGUAGES
import logging
from flask.logging import default_handler

db = SQLAlchemy()
babel = Babel()

def create_app(script_info):
    # if evoked from "flask shell", get the env ourselves,
    # since manage.py does this for us otherwise.
    if type(script_info) is str:
        config_name = script_info
    else:
        config_name = os.getenv('APP_CONFIG')
    os.environ['FLASK_ENV'] = config_name
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['NAV'] = os.getenv('NAV')
    config[config_name].init_app(app)
    db.init_app(app)
    babel.init_app(app)

    # logging config
    app.logger.setLevel(os.getenv('LOG_LEVEL', default='WARN'))
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    default_handler.setFormatter(formatter)

    @babel.localeselector
    def get_locale():
        from app.main.helpers import guess_locale
        if g.locale:
            return g.locale
        return guess_locale()

    @app.url_defaults
    def set_language_code(endpoint, values):
        if 'lang_code' in values or not g.get('lang_code', None):
            return
        if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
            values['lang_code'] = g.lang_code

    @app.url_value_preprocessor
    def get_lang_code(endpoint, values):
        if values is not None:
            g.lang_code = values.pop('lang_code', None)

    @app.before_request
    def ensure_lang_support():
        lang_code = g.get('lang_code', None)
        if lang_code and lang_code not in LANGUAGES.keys():
            return abort(404)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(main_blueprint, url_prefix='/<lang_code>')

    return app
