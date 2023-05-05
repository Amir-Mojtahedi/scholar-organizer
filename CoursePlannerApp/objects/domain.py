"""Modules providing form and validation for forms"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class Domain:
    '''Class representing Domain object'''
    def __init__(self, id, name, description):
        if not isinstance(id, int):  # Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.id = id
        if not isinstance(name, str):  # Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
        if not isinstance(description, str):  # Description validation
            raise TypeError("Enter a valid Description. Try again.")
        self.description = description

    def __repr__(self):
        return f'{self.name}: {self.id}, {self.description}'

    def __str__(self):
        return f'<h3>{self.name}: </h3> \
                    <ul>    \
                            <li> ID: {self.id}</li> \
                            <li> Description: {self.description}</li>   \
                    </ul>'

class DomainForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    description = StringField('Domain Description',validators=[DataRequired()])
