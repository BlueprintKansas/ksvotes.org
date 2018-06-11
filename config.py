# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "devsk"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

class ProductionConfig(Config):
    JSONIFY_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

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
