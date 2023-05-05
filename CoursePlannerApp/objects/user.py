from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import EmailField, PasswordField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length


class User(UserMixin):
    """Class representing User"""
    def __init__(self, id, group_id, name, email, password, blocked=False):
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
        self.blocked = blocked

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return not self.blocked


class UserForm(FlaskForm):
    """Form for User object"""
    id = IntegerField("id")
    group_id = IntegerField("group_id")
    name = StringField("Name")


class SignupForm(FlaskForm):
    """Form used to Sign Up user"""
    email = EmailField("Email", validators=[DataRequired(), Length(1, 50)])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    id = IntegerField("id")
    group_id = IntegerField("group_id")
    avatar = FileField('Avatar')

class EditForm(FlaskForm):
    """For, to edit User object"""
    email = EmailField("Email", validators=[DataRequired(), Length(1, 50)])
    password = PasswordField("Password")
    name = StringField("Name", validators=[DataRequired(), Length(1, 30)])
    id = IntegerField("id")
    group_id = IntegerField("group_id")
    avatar = FileField('Avatar')

class LoginForm(FlaskForm):
    """Form used to Login User"""
    email = EmailField("Email", validators=[DataRequired(), Length(1, 50)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")


class ChangePasswordForm(FlaskForm):
    """Form used to Change Password of User"""
    old_password = PasswordField("Enter your old password: ", validators=[DataRequired()])
    new_password = PasswordField("Enter your new password: ", validators=[DataRequired()])
