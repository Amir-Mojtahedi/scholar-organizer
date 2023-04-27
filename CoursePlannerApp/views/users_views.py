import oracledb
from flask import Blueprint, redirect, render_template, flash, url_for
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.user import SignupForm, User, UserForm

bp = Blueprint("users", __name__, url_prefix="/users/")

dtb = LocalProxy(get_db)


@bp.route("/")
@login_required
def index():
    form = SignupForm()

    # get user
    user = current_user
    level = user.group_id

    # get all users
    try:
        users = dtb.get_users()
    except oracledb.Error:
        flash("There was an error retrieving the users from the database")
        users = []

    # get all groups
    try:
        groups = dtb.get_groups()
    except oracledb.Error:
        flash("There was an error retrieving the groups from the database")
        groups = []

    if level == 0 or level == 1:  # members and admin_user_gp can see members
        group = [g for g in groups if g.id == 0][0]
        group.users = [u for u in users if u.group_id == 0]
        return render_template("users.html", manages=level == 1, groups=[group], users=users, form=form)

    elif level == 2:  # admin_gp can see all users and groups
        # insert users into each group
        for group in groups:
            group.users = [u for u in users if u.group_id == group.id]

        return render_template("users.html", manages=True, groups=groups, form=form)
    

@bp.route("/", methods=["POST"])
@login_required
def add():
    form = SignupForm()

    # get authorization level
    if form.validate_on_submit():
        if current_user.group_id == 0:
            flash("You don't have permission to add users")
            return redirect(url_for(".index"))

        if form.group_id.data in [1, 2] and current_user.group_id != 2:
            flash("You don't have permission to add users to this group")
            return redirect(url_for(".index"))
        
        user = User(name=form.name.data, avatar=form.avatar.data, email=form.email.data, password=form.password.data, group_id=form.group_id.data)

    flash("Invalid form data")
    return redirect(url_for(".index"))


@bp.route("/delete/", methods=["POST"])
@login_required
def delete():
    form = UserForm()

    # get user
    user = current_user
    manages = user.group_id == 1 or user.group_id == 2

    if not manages:
        flash("You don't have permission to edit users")
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        user = User(id=form.id.data)

        # try to delete user
        try:
            dtb.delete_user(user)
        except oracledb.Error:
            flash("There was an error deleting the user from the database")
            return redirect(url_for(".index"))

        flash("User deleted successfully")
        return redirect(url_for(".index"))

    else:
        flash("Invalid form data")
        return redirect(url_for(".index"))
