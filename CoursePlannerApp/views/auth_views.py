import shutil
import oracledb
import os
from flask import Blueprint, redirect, render_template, request, url_for, flash, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.local import LocalProxy
from werkzeug.security import check_password_hash, generate_password_hash

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.user import LoginForm, SignupForm, ChangePasswordForm, User

bp = Blueprint("auth", __name__, url_prefix="/auth/")

dtb = LocalProxy(get_db)


@bp.route("/signup/", methods=["GET", "POST"])
def signup():
    """Function used to create a new user"""
    form = SignupForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                db_user = dtb.get_user_by_email(form.email.data)
            except oracledb.Error as e:
                flash("Error: " + str(e))
                return render_template("signup.html", form=form)

            if db_user:
                flash("User with this email already exists")
            else:
                file = form.avatar.data
                if file:
                    avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                    avatar_path = os.path.join(avatar_dir, 'avatar.png')
                    if not os.path.exists(avatar_dir):
                        os.makedirs(avatar_dir)
                    file.save(avatar_path)
                else:
                    # If no file for the profile picture is
                    # # provided by the user, the default path
                    # will be set to a profile icon which is
                    # saved in images directory(not the one in instance).
                    # os.getcwd() gets the current working
                    # directory which in our case is the root of the repository
                    default_avatar_path = os.path.join(os.getcwd(), 'CoursePlannerApp\\images\\avatar.png')
                    avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                    avatar_path = os.path.join(avatar_dir,'avatar.png')
                    if not os.path.exists(avatar_dir):
                        os.makedirs(avatar_dir)
                    # shutil.copy() is like save() but the big difference is that it does 
                    # not need a file, however, it retrieves the file that the path is pointing to e.g. avatar.png.
                    # Using it, we retrieve the default profile picture and set it to avatar_path
                    # which will allow show_avatar() to successfuly retrieve the right image which
                    # in this case is the default one.
                    shutil.copy(default_avatar_path, avatar_path)
                _hash = generate_password_hash(form.password.data)
                user = User(None, 0, form.name.data, form.email.data, _hash)
                dtb.add_user(user)
        else:
            flash("Form is not valid")

    return render_template("signup.html", form=form)


@bp.route("/login/", methods=["GET", "POST"])
def login():
    """Function used to login user"""
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = dtb.get_user_by_email(form.email.data)
            except oracledb.Error as e:
                flash("Error: " + str(e))
                return render_template("login.html", form=form)

            if user:
                if user.blocked:
                    return render_template("blocked.html")
                else:
                    if check_password_hash(user.password, form.password.data):
                        login_user(user, form.remember_me.data)
                    else:
                        flash("Incorrect credentials")
            else:
                flash("No user exists with this email")
        else:
            flash("Form isn't valid")

    return render_template("login.html", form=form)


@bp.route("/logout/")
@login_required
def logout():
    """Function used to logout a user"""
    logout_user()
    return redirect(url_for("auth.login"))

@bp.route('/profile/<email>/change-password/', methods=["GET", "POST"])
@login_required
def change_password(email):
    """Function used to change a user's password"""
    form = ChangePasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
                try:
                    user = dtb.get_user_by_email(email)
                    if check_password_hash(user.password, form.old_password.data):
                        _hash = generate_password_hash(form.new_password.data)
                        user.password=_hash
                        dtb.update_user(user)
                        flash("Password was changed successfuly")
                    else:
                        flash("Incorrect password")
                except oracledb.Error as e:
                    flash("Error: " + str(e))
                    return redirect("change_password.html")  
        else:
            flash("Form isn't valid")
    return render_template("change_password.html", form=form)

@bp.route('/profile/<email>/', methods=["GET", "POST"])
@login_required
def change_avatar(email):
    """Function used to change the avatar of a user"""
    form = SignupForm()
    if request.method == "POST":
        file = form.avatar.data
        avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], email)
        avatar_path = os.path.join(avatar_dir, 'avatar.png')
        file.save(avatar_path)
    return render_template("avatar.html", form=form)


@bp.route('/avatars/<email>/avatar.png')
def show_avatar(email):
    """Function used to show a user's avatar"""
    path = os.path.join(current_app.config['IMAGE_PATH'], email)
    return send_from_directory(path, 'avatar.png')
