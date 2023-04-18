from flask import Blueprint, render_template, flash, render_template, request, redirect, url_for    
from werkzeug.local import LocalProxy
from CoursePlannerApp.dbmanager import get_db




import oracledb

dtb = LocalProxy(get_db)

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/", methods=['GET', 'POST'])
def index():
    return redirect(url_for("courses.get_courses"))










