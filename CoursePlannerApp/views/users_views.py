import os
import shutil

import oracledb
from flask import Blueprint, redirect, render_template, flash, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy
from werkzeug.security import generate_password_hash

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.user import EditForm, User, UserForm

bp = Blueprint("users", __name__, url_prefix="/users/")
dtb = LocalProxy(get_db)


@bp.route("/")
@login_required
def index():
    form = EditForm()

    # get authorization level
    level = current_user.group_id

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

    if level == 2:  # admin_gp can see all users and groups
        for group in groups:
            group.users = [u for u in users if
                           u.group_id == group.id]  # inserting users in group for nested loop usability

        return render_template("users.html", manages=True, groups=groups, form=form)
    else:  # members, other groups and admin_user_gp can see members (only admin_user_gp can manage them)
        group = [g for g in groups if g.id == 0][0]
        group.users = [u for u in users if u.group_id == 0]  # inserting users in group for nested loop usability

        return render_template("users.html", manages=level == 1, groups=[group], form=form)


@bp.route("/", methods=["POST"])
@login_required
def add():
    form = EditForm()

    if form.validate_on_submit():
        check_authorization(form.group_id.data)

        # get user by email
        try:
            db_user = dtb.get_user_by_email(form.email.data)
        except oracledb.Error:
            flash("There was an error retrieving the user from the database")
            return redirect(url_for(".index"))

        # taken as is from auth_views.py
        if db_user:
            flash("User with this email already exists")
            return redirect(url_for(".index"))
        else:
            file = form.avatar.data
            if file:
                avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                avatar_path = os.path.join(avatar_dir, 'avatar.png')
                if not os.path.exists(avatar_dir):
                    os.makedirs(avatar_dir)
                file.save(avatar_path)
            else:
                default_avatar_path = os.path.join(os.getcwd(), 'CoursePlannerApp', 'images', 'avatar.png')
                avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                avatar_path = os.path.join(avatar_dir, 'avatar.png')

                if not os.path.exists(avatar_dir):
                    os.makedirs(avatar_dir)

                shutil.copy(default_avatar_path, avatar_path)

            _hash = generate_password_hash(form.password.data)
            user = User(None, form.group_id.data, form.name.data, form.email.data, _hash)

            # add user
            try:
                dtb.add_user(user)
            except oracledb.Error:
                flash("There was an error adding the user to the database")
                return redirect(url_for(".index"))

            flash("User added successfully")
            return redirect(url_for(".index"))

    flash("Invalid form data")
    return redirect(url_for(".index"))


@bp.route("/edit/", methods=["POST"])
@login_required
def edit():
    form = EditForm()

    if form.validate_on_submit():
        check_authorization(form.group_id.data)

        # get user by email
        try:
            db_user = dtb.get_user_by_email(form.email.data)
        except oracledb.Error:
            flash("There was an error retrieving the user from the database")
            return render_template("signup.html", form=form)

        if db_user and db_user.id != form.id.data:
            flash("User with this email already exists")
            return redirect(url_for(".index"))
        else:
            file = form.avatar.data
            if file:
                avatar_path = os.path.join(current_app.config['IMAGE_PATH'], form.email.data, 'avatar.png')

                # remove old avatar
                if os.path.exists(avatar_path):
                    os.remove(avatar_path)
                else:  # save new avatar
                    os.makedirs(os.path.join(current_app.config['IMAGE_PATH'], form.email.data))

                file.save(avatar_path)

        # if we keep password as is
        if not form.password.data:
            # get password from database
            try:
                password = dtb.get_user(form.id.data).password
            except oracledb.Error:
                flash("There was an error retrieving the user from the database")
                return redirect(url_for(".index"))
        else:
            password = generate_password_hash(form.password.data)

        user = User(form.id.data, form.group_id.data, form.name.data, form.email.data, password)

        # edit user
        try:
            dtb.update_user(user)
        except oracledb.Error:
            flash("There was an error editing the user in the database")
            return redirect(url_for(".index"))

        flash("User edited successfully")
        return redirect(url_for(".index"))

    flash("Invalid form data")
    return redirect(url_for(".index"))


@bp.route("/delete/", methods=["POST"])
@login_required
def delete():
    form = UserForm()

    if form.validate_on_submit():
        check_authorization(form.group_id.data)

        # delete user
        try:
            dtb.delete_user_by_id(form.id.data)
        except oracledb.Error:
            flash("There was an error deleting the user from the database")
            return redirect(url_for(".index"))

        flash("User deleted successfully")
        return redirect(url_for(".index"))

    flash("Invalid form data")
    return redirect(url_for(".index"))


@bp.route("/block/", methods=["POST"])
@login_required
def block():
    form = UserForm()

    if form.validate_on_submit():
        check_authorization(form.group_id.data)

        # get user
        try:
            user = dtb.get_user(form.id.data)
        except oracledb.Error:
            flash("There was an error retrieving the user from the database")
            return redirect(url_for(".index"))

        # block user
        user.blocked = True

        # update user
        try:
            dtb.update_user(user)
        except oracledb.Error:
            flash("There was an error updating the user in the database")
            return redirect(url_for(".index"))

        flash("User blocked successfully")
        return redirect(url_for(".index"))

    flash("Invalid form data")
    return redirect(url_for(".index"))


@bp.route("/unblock/", methods=["POST"])
@login_required
def unblock():
    form = UserForm()

    if form.validate_on_submit():
        check_authorization(form.group_id.data)

        # get user
        try:
            user = dtb.get_user(form.id.data)
        except oracledb.Error:
            flash("There was an error retrieving the user from the database")
            return redirect(url_for(".index"))

        # unblock user
        user.blocked = False

        # update user
        try:
            dtb.update_user(user)
        except oracledb.Error:
            flash("There was an error updating the user in the database")
            return redirect(url_for(".index"))

        flash("User unblocked successfully")
        return redirect(url_for(".index"))

    flash("Invalid form data")
    return redirect(url_for(".index"))


def check_authorization(group_id):
    # get authorization level
    level = current_user.group_id

    if level == 0 or level > 2:  # members and other groups can't manage users
        flash("You don't have permission to add users")
        return redirect(url_for(".index"))

    if level != 2 and group_id in [1, 2]:  # only admin_gp can manage admin_gp and admin_user_gp
        flash("You don't have permission to add users to this group")
        return redirect(url_for(".index"))
