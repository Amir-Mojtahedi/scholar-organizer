from flask import Flask, render_template
# from .dbmanager import close_db,init_db_command
# from .address_views import bp as address_bp
# from .home_view import bp as home_bp
# from .address_api import bp as addressapi_bp
import secrets

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_urlsafe(32),
    )
    with app.app_context():
        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)
        # init_app(app=app)
        
        # @app.errorhandler(404)
        # def page_not_found(error):
        #     return render_template('custom404.html')
        # return app

# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(init_db_command)
#     app.register_blueprint(address_bp)
#     app.register_blueprint(home_bp)
#     app.register_blueprint(addressapi_bp)
    
