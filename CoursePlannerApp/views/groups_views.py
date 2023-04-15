import oracledb
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.group import GroupForm, Group

bp = Blueprint("groups", __name__, url_prefix="/groups/")

dtb = LocalProxy(get_db)


@bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    form = GroupForm()

    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2  # admin_user_gp or admin_gp (respectively)

    # get all groups
    try:
        groups = dtb.get_groups()
    except oracledb.Error:
        flash("There was an error retrieving the groups from the database")
        groups = []

    if request.method == "GET":
        return render_template("groups.html", manages=manages, groups=groups, form=form)

    elif request.method == "POST" and form.validate_on_submit():
        group = Group(name=form.name.data)

        # check if it already exists, by name from groups
        if group.name in [g.name for g in groups]:
            flash("Group already exists")
            return redirect(url_for(".index"))

        # try to add group
        try:
            dtb.add_group(group)
        except oracledb.Error:
            flash("There was an error adding the group to the database")
            return redirect(url_for(".index"))

        flash("Group added successfully")
        return redirect(url_for(".index"))
    else:
        flash("Invalid form data")
        return redirect(url_for(".index"))
