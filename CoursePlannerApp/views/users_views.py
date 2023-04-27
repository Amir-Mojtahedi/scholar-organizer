import os
import shutil

import oracledb
from flask import Blueprint, redirect, render_template, flash, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.local import LocalProxy
from werkzeug.security import generate_password_hash

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.user import EditForm, SignupForm, User, UserForm

bp = Blueprint("users", __name__, url_prefix="/users/")

dtb = LocalProxy(get_db)


@bp.route("/")
@login_required
def index():
    form = EditForm()

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
    form = EditForm()

    # get authorization level
    if form.validate_on_submit():
        if current_user.group_id == 0:
            flash("You don't have permission to add users")
            return redirect(url_for(".index"))

        if form.group_id.data in [1, 2] and current_user.group_id != 2:
            flash("You don't have permission to add users to this group")
            return redirect(url_for(".index"))

        try:
            db_user = dtb.get_user_by_email(form.email.data)
        except oracledb.Error as e:
            flash("Error: " + str(e))
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
                # If no file for the profile picture is provided by the user, the default path will
                # be set to a profile icon which is saved in images directory(not the one in instance).
                # os.getcwd() gets the current working directory which in our case is the root of the repository
                default_avatar_path = os.path.join(os.getcwd(), 'CoursePlannerApp', 'images', 'avatar.png')
                avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                avatar_path = os.path.join(avatar_dir, 'avatar.png')
                if not os.path.exists(avatar_dir):
                    os.makedirs(avatar_dir)
                # shutil.copy() is like save() but the big difference is that it does not need a file, however, it retrieves the file that the path is pointing to e.g. avatar.png.
                # Using it, we retrieve the default profile picture and set it to avatar_path which will allow show_avatar()
                # to successfuly retrieve the right image which in this case is the default one.
                shutil.copy(default_avatar_path, avatar_path)
            _hash = generate_password_hash(form.password.data)
            user = User(None, form.group_id.data, form.name.data, form.email.data, _hash)

            # try to add user
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

    if current_user.group_id == 0:
        flash("You don't have permission to edit users")
        return redirect(url_for(".index"))

    if form.group_id.data in [1, 2] and current_user.group_id != 2:
        flash("You don't have permission to edit users from this group")
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        # taken as is from auth_views.py
        try:
            db_user = dtb.get_user_by_email(form.email.data)
        except oracledb.Error as e:
            flash("Error: " + str(e))
            return render_template("signup.html", form=form)

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
                # If no file for the profile picture is provided by the user, the default path will
                # be set to a profile icon which is saved in images directory(not the one in instance).
                # os.getcwd() gets the current working directory which in our case is the root of the repository
                default_avatar_path = os.path.join(os.getcwd(), 'CoursePlannerApp', 'images', 'avatar.png')
                avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                avatar_path = os.path.join(avatar_dir, 'avatar.png')
                if not os.path.exists(avatar_dir):
                    os.makedirs(avatar_dir)
                # shutil.copy() is like save() but the big difference is that it does not need a file, however, it retrieves the file that the path is pointing to e.g. avatar.png.
                # Using it, we retrieve the default profile picture and set it to avatar_path which will allow show_avatar()
                # to successfuly retrieve the right image which in this case is the default one.
                shutil.copy(default_avatar_path, avatar_path)

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

        # try to edit user
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

    if current_user.group_id == 0:
        flash("You don't have permission to delete users")
        return redirect(url_for(".index"))

    if form.group_id.data in [1, 2] and current_user.group_id != 2:
        flash("You don't have permission to delete users from this group")
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        # try to delete user
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

    if current_user.group_id == 0:
        flash("You don't have permission to block users")
        return redirect(url_for(".index"))

    if form.group_id.data in [1, 2] and current_user.group_id != 2:
        flash("You don't have permission to block users from this group")
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        # try to get user
        try:
            user = dtb.get_user(form.id.data)
        except oracledb.Error:
            flash("There was an error retrieving the user from the database")
            return redirect(url_for(".index"))

        # block user
        user.blocked = True

        # try to update user
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

    if current_user.group_id == 0:
        flash("You don't have permission to unblock users")
        return redirect(url_for(".index"))

    if form.group_id.data in [1, 2] and current_user.group_id != 2:
        flash("You don't have permission to unblock users from this group")
        return redirect(url_for(".index"))

    if form.validate_on_submit():
        # try to get user
        try:
            user = dtb.get_user(form.id.data)
        except oracledb.Error:
            flash("There was an error retrieving the user from the database")
            return redirect(url_for(".index"))

        # unblock user
        user.blocked = False

        # try to update user
        try:
            dtb.update_user(user)
        except oracledb.Error:
            flash("There was an error updating the user in the database")
            return redirect(url_for(".index"))

        flash("User unblocked successfully")
        return redirect(url_for(".index"))

    flash("Invalid form data")
    return redirect(url_for(".index"))