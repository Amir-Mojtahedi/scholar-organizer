import os
from .dbmanager import close_db, init_db_command,get_db
from flask import Flask, render_template, current_app
import secrets
import click
from flask_login import LoginManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secrets.token_urlsafe(32))

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return get_db().get_user_by_id(int(user_id))

    from .home_views import bp as home_bp
    app.register_blueprint(home_bp)

    from .auth_views import bp as auth_bp
    app.register_blueprint(auth_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('custom404.html'), 404
    
    init_app(app)

    return app

def init_app(app):
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)
