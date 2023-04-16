<<<<<<< HEAD
import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
bp = Blueprint('display', __name__, url_prefix='/display')
=======
from flask import Blueprint, render_template, url_for
>>>>>>> c7eaf0cff7898ee98236e82dd1e1c5d26afdcdce

bp = Blueprint('display', __name__, url_prefix='/display')

#HOMEPAGE
@bp.route("/")
def display():
    return render_template('display.html')

