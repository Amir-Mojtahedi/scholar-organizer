from flask import Blueprint,redirect,render_template,request,url_for,flash
from CoursePlannerApp.dbmanager import get_db
from CoursePlannerApp.user import LoginForm,SignupForm,User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user,login_required

bp=Blueprint('auth',__name__,url_prefix='/auth/')

@bp.route('/signup/',methods=['GET','POST'])
def signup():
    form=SignupForm()
    if request.methdo=='POST':
        if form.validate_on_submit():
            if get_db().get_user(form.email.data):
                flash("User with this email already exists")
            else:
                hash=generate_password_hash(form.password.data)
                user=User(form.email.data,hash,form.name.data)
                get_db().add_user(user)
    return render_template('signup.html',form=form)
