import os

from flask import Flask
from .dbmanager import close_db, init_db_command

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=os.environ['SECRET'])

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    init_app(app)

    return app

def init_app(app):
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)
