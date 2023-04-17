import oracledb
from flask import Blueprint, flash, render_template, request
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db
bp = Blueprint('add', __name__, url_prefix='/add')

dtb = LocalProxy(get_db)

#Add Page
@bp.route("/")
def display():
    return render_template('addEntities.html')

