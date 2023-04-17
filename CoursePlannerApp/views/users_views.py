import oracledb
from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db

bp = Blueprint("users", __name__, url_prefix="/users/")

dtb = LocalProxy(get_db)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2  # admin_user_gp or admin_gp (respectively)

    # get all groups
    try:
        users = dtb.get_users()
    except oracledb.Error:
        flash("There was an error retrieving the users from the database")
        users = []

    if request.method == "GET":
        return render_template("users.html", manages=manages, users=users)
