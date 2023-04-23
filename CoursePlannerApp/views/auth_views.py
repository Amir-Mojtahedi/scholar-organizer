import oracledb
import os
from flask import Blueprint, redirect, render_template, request, url_for, flash, send_from_directory, current_app
from flask_login import login_user, logout_user, login_required
from werkzeug.local import LocalProxy
from werkzeug.security import check_password_hash, generate_password_hash

from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.objects.user import LoginForm, SignupForm, User

bp = Blueprint("auth", __name__, url_prefix="/auth/")

dtb = LocalProxy(get_db)


@bp.route("/signup/", methods=["GET", "POST"])
def signup():
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
                avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], form.email.data)
                avatar_path = os.path.join(avatar_dir, 'avatar.png')
                if not os.path.exists(avatar_dir):
                    os.makedirs(avatar_dir)
                file.save(avatar_path)
                _hash = generate_password_hash(form.password.data)
                user = User(form.email.data, form.name.data, _hash)
                dtb.add_user(user)
        else:
            flash("Form is not valid")

    return render_template("signup.html", form=form)


@bp.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = dtb.get_user_by_email(form.email.data)
            except oracledb.Error as e:
                flash("Error: " + str(e))
                return render_template("login.html", form=form)

            if user:
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
    logout_user()
    return redirect(url_for("auth.login"))

@bp.route('/avatars/<email>/avatar.png')
def show_avatar(email):
    path = os.path.join(current_app.config['IMAGE_PATH'], email)
    return send_from_directory(path, 'avatar.png')

