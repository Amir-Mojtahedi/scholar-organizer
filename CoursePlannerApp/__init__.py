import secrets

from flask import Flask, render_template
from flask_login import LoginManager

from .auth_views import bp as auth_bp
from .dbmanager import close_db, init_db_command, get_db
from .home_views import bp as home_bp
from .competency_api import bp as competencyApi_bp
from .competency_views import bp as competencyViews_bp
from .element_api import bp as elementApi_bp
from .element_views import bp as elementViews_bp
from .course_api import bp as courseApi_bp
from .course_views import bp as courseViews_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secrets.token_urlsafe(32))

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_db().get_user_by_id(int(user_id))

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)

    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("custom404.html"), 404

    init_app(app)
    return app


def init_app(app):
    #DbManager
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)

    #CompetencyApi
    app.register_blueprint(competencyApi_bp)
    
    #CompetencyViews
    app.register_blueprint(competencyViews_bp)
    
    #ElementApi
    app.register_blueprint(elementApi_bp)
    
    #ElementViews
    app.register_blueprint(elementViews_bp)
    
    #CourseApi
    app.register_blueprint(courseApi_bp)
    
    #CourseViews
    app.register_blueprint(courseViews_bp)