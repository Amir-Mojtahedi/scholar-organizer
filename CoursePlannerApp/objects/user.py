from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired


class User(UserMixin):
    def __init__(self, email, name, password=None, id=None, group_id=0):
        if not isinstance(email, str):
            raise TypeError("E-mail must be a string")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if id and not isinstance(id, int):
            raise TypeError("Id must be an integer")
        if group_id and not isinstance(group_id, int):
            raise TypeError("Group id must be an integer")

        self.email = email
        self.password = password
        self.name = name
        self.id = id
        self.group_id = group_id


class SignupForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    avatar = FileField('avatar')


class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember me")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Enter your old password: ", validators=[DataRequired()])
    new_password = PasswordField("Enter your new password: ", validators=[DataRequired()])
