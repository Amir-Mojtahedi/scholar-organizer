import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
bp = Blueprint('display', __name__, url_prefix='/display')

#HOMEPAGE
@bp.route("/")
def display():
    return redirect(url_for('courses.get_courses'))

