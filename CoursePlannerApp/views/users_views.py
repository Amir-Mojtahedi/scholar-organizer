import oracledb
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db

bp = Blueprint("users", __name__, url_prefix="/users/")

dtb = LocalProxy(get_db)


@bp.route("/")
@login_required
def index():
    # get user
    user = current_user
    level = user.group_id

    # get all users
    try:
        users = dtb.get_users()
    except oracledb.Error:
        flash("There was an error retrieving the users from the database")
        users = []

    if level == 0 or level == 1:  # members and admin_user_gp can see members
        users = [u for u in users if u.group_id == 0]
        return render_template("users.html", manages=level == 1, groups=[], users=users)

    elif level == 2:  # admin_gp can see all users and groups
        # get all groups
        try:
            groups = dtb.get_groups()
        except oracledb.Error:
            flash("There was an error retrieving the groups from the database")
            groups = []

        # insert a group into each user
        for u in users:
            u.group = next(g for g in groups if g.id == u.group_id)

        return render_template("users.html", manages=True, groups=groups, users=users)
