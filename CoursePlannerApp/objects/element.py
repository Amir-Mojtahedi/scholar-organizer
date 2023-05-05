"""Modules providing form and validation for forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange


class Element:
    '''Class representing Element object'''

    def __init__(self, id, order, name, criteria, competency_id):
        if not isinstance(id, int):  # Id validation
            raise TypeError("Enter a valid number. Try again.")
        self.id = id
        if not isinstance(order, int):  # Order validation
            raise TypeError("Enter a valid number. Try again.")
        self.order = order
        if not isinstance(name, str):  # Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
        if not isinstance(criteria, str):  # Criteria validation
            raise TypeError("Enter a valid criteria. Try again.")
        self.criteria = criteria
        if not isinstance(competency_id, str):  # Competency validation
            raise TypeError(
                "Enter a the Id of a valid/existing competency. Try again.")
        self.competency_id = competency_id

    def __repr__(self):
        return f'{self.name}: {self.id}, {self.order}, {self.criteria}, \
                    {self.competency_id}'

    def __str__(self):
        return f'<h3>{self.name} </h3> \
                    <ul>    \
                            <li> ID: {self.id}</li> \
                            <li> Order: {self.order}</li>   \
                            <li> Criteria: {self.criteria}</li> \
                            <li> Competency ID: {self.competency_id}</li>    \
                    </ul>'


class ElementForm(FlaskForm):
    '''Form for Element object'''
    order = IntegerField('Order', validators=[DataRequired(),
                                              NumberRange(min=1)
                                              ])
    name = StringField('Name', validators=[DataRequired()])
    criteria = StringField('Criteria', validators=[DataRequired()])
    competency_id = SelectField('Id of associated Competency',
                               validators=[DataRequired()], choices=[])


class ElementFormBridge(FlaskForm):
    '''Form for Element object Bridging tbl'''
    id = SelectField('Id of associated Element', validators=[
                     DataRequired()], choices=[])
    element_hours = IntegerField('How many hours does this element take', validators=[DataRequired(),
                                 NumberRange(min=1)
    ])
