import os
import secrets

from flask import Flask, render_template
from flask_login import LoginManager

from CoursePlannerApp.apis.domains_api import bp as domains_api
from CoursePlannerApp.apis.terms_api import bp as terms_api
from CoursePlannerApp.apis.courses_api import bp as courses_api
from CoursePlannerApp.apis.competencies_api import bp as competencies_api
from CoursePlannerApp.apis.elements_api import bp as elements_api
from CoursePlannerApp.views.auth_views import bp as auth_bp
from CoursePlannerApp.views.competency_views import bp as competency_bp
from CoursePlannerApp.views.course_views import bp as course_bp
from CoursePlannerApp.views.display_views import bp as display_bp
from CoursePlannerApp.views.domain_views import bp as domain_bp
from CoursePlannerApp.views.element_views import bp as element_bp
from CoursePlannerApp.views.groups_views import bp as groups_bp
from CoursePlannerApp.views.home_views import bp as home_bp
from CoursePlannerApp.views.term_views import bp as term_bp
from CoursePlannerApp.views.users_views import bp as users_bp
from .dbmanager import close_db, init_db_command, get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secrets.token_urlsafe(32), IMAGE_PATH=os.path.join(app.instance_path, 'images'))

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_db().get_user(int(user_id))

    @app.errorhandler(404)
    def page_not_found(_):
        return render_template("custom404.html"), 404

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['IMAGE_PATH'], exist_ok=True)

    init_app(app)
    return app


def init_app(app):
    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(display_bp)
    app.register_blueprint(competency_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(domain_bp)
    app.register_blueprint(element_bp)
    app.register_blueprint(term_bp)

    app.register_blueprint(groups_bp)
    app.register_blueprint(users_bp)

    app.register_blueprint(domains_api)
    app.register_blueprint(terms_api)
    app.register_blueprint(courses_api)
    app.register_blueprint(competencies_api)
    app.register_blueprint(elements_api)
