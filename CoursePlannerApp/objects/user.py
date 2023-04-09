from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, password, name, id=None):
        if not isinstance(email, str):
            raise TypeError("E-mail must be a string")
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if id and not isinstance(id, int):
            raise TypeError("Id must be an integer")
        self.email = email
        self.password = password
        self.name = name
        self.id = id

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    email=EmailField('email',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    name=StringField('name',validators=[DataRequired()])

class LoginForm(FlaskForm):
    email=EmailField('email',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    remember_me=BooleanField('remember me')