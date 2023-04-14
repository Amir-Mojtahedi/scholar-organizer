import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
bp = Blueprint('display', __name__, url_prefix='/display')

dtb = LocalProxy(get_db)

#Display Page
@bp.route("/")
def display():
    return render_template('display.html')

