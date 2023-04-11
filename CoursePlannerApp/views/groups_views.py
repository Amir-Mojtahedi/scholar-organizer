import oracledb
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db

bp = Blueprint("groups", __name__, url_prefix="/groups/")

dtb = LocalProxy(get_db)


@bp.route("/")
@login_required
def index():
    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2  # admin_user_gp or admin_gp (respectively)

    # get all groups
    try:
        groups = dtb.get_groups()
    except oracledb.Error:
        flash("There was an error retrieving the groups from the database")
        groups = []

    return render_template("groups.html", manages=manages, groups=groups)
