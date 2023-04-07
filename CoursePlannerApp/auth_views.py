import oracledb
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from .dbmanager import get_db
from .user import LoginForm, SignupForm, User

bp = Blueprint("auth", __name__, url_prefix="/auth/")


@bp.route("/signup/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    db = get_db()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                db_user = db.get_user(form.email.data)
            except oracledb.Error as e:
                flash("Error: " + str(e))
                return render_template("signup.html", form=form)

            if db_user:
                flash("User with this email already exists")
            else:
                _hash = generate_password_hash(form.password.data)
                user = User(form.email.data, _hash, form.name.data)
                db.add_user(user)
        else:
            flash("Form is not valid")

    return render_template("signup.html", form=form)


@bp.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    db = get_db()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = db.get_user(form.email.data)
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
