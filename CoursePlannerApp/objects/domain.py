"""Modules providing form and validation for forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class Domain:
    '''Class representing Domain object'''
    def __init__(self, id, name, description):
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

    def from_json(domain_dict):
        '''Create Domain object from Json'''
        if not isinstance(domain_dict,dict):
            raise TypeError("Expected dict")
        return Domain(domain_dict['id'],domain_dict['name'],domain_dict['description'])

    def to_json(domain):
        '''Return in json format'''
        if not isinstance(domain,Domain):
            raise TypeError("Expected Address")
        return domain.__dict__

class DomainForm(FlaskForm):
    '''Form for Domain object'''
    id = IntegerField('Id')
    name = StringField('Name',validators=[DataRequired()])
    description = StringField('Domain Description',validators=[DataRequired()])
