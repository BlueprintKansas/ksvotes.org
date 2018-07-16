# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "devsk"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET')
    BABEL_DEFAULT_LOCALE = 'en'
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@ksvotes.org')
    AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    SEND_EMAIL = os.getenv('SEND_EMAIL')
    SSL_DISABLE = os.getenv('SSL_DISABLE', False)
    SESSION_TTL = os.getenv('SESSION_TTL', '10')
    DEMO_UUID = os.getenv('DEMO_UUID', None)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_DATABASE_URL")
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True if os.getenv('SQL_DEBUG') else False

class ProductionConfig(Config):
    JSONIFY_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    GA_KEY = os.environ.get('GA_KEY')

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}
