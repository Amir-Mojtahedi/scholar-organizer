from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class Group:
    def __init__(self, name, id=None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if id and not isinstance(id, int):
            raise TypeError("Id must be an integer")

        self.name = name
        self.id = id

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"


class GroupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    id = IntegerField("Id")
