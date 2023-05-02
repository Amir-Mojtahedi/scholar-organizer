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

    if current_user.group_id != 2:
        flash("You don't have permission to manage groups")
        return redirect(url_for("home.index"))

    # get all groups
    try:
        groups = dtb.get_groups()
    except oracledb.Error:
        flash("There was an error retrieving the groups from the database")
        groups = []

    if request.method == "GET":
        return render_template("groups.html", manages=current_user.group_id == 2, groups=groups, form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            group = Group(form.name.data)

            # check if it already exists, by name from groups
            if group.name in [g.name for g in groups]:
                flash("Group already exists")
                return redirect(url_for(".index"))

            # add group
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


@bp.route("/edit/", methods=["POST"])
@login_required
def edit():
    form = GroupForm()

    if current_user.group_id != 2:
        flash("You don't have permission to manage groups")
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        # get db group
        try:
            dbgroup = dtb.get_group(form.id.data)
        except oracledb.Error:
            flash("There was an error retrieving the group from the database")
            return redirect(url_for(".index"))

        if not dbgroup:
            flash("Group not found")
            return redirect(url_for(".index"))

        # update group
        try:
            dbgroup.name = form.name.data
            dtb.update_group(dbgroup)
        except oracledb.Error:
            flash("There was an error editing the group in the database")
            return redirect(url_for(".index"))

        flash("Group edited successfully")
        return redirect(url_for(".index"))
    else:
        flash("Invalid form data")
        return redirect(url_for(".index"))


@bp.route("/delete/", methods=["POST"])
@login_required
def delete():
    form = GroupForm()

    if current_user.group_id != 2:
        flash("You don't have permission to manage groups")
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        group = Group(form.name.data, form.id.data)

        # delete group
        try:
            dtb.delete_group(group)
        except oracledb.Error:
            flash("There was an error deleting the group from the database")
            return redirect(url_for(".index"))

        flash("Group deleted successfully")
        return redirect(url_for(".index"))
    else:
        flash("Invalid form data")
        return redirect(url_for(".index"))
