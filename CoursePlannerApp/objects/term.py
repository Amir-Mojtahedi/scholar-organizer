from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired

class Term:
    def __init__(self, id, name):
        if not isinstance(id, int):  # Id validation
            raise TypeError("Enter a valid id. Try again.")
        self.id = id
        if not isinstance(name, str):  # Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name

    def __repr__(self):
        return f'{self.name}: {self.id}'

    def __str__(self):
        return f'<h3> Term ID: {self.id}: </h3> \
                    <ul>    \
                            <li> Season: {self.name}</li> \
                    </ul>'

class TermForm(FlaskForm):
    id = IntegerField('Id',validators=[DataRequired()])
    name = StringField('Name',validators=[DataRequired()])
