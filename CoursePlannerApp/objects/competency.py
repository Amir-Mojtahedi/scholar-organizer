from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Regexp

class Competency:
    def __init__(self, id, name, achievement, type):
        if not isinstance(id, str):  # Id validation
            raise TypeError("Enter a valid Id. Try again.")
        self.id = id
        if not isinstance(name, str):  # Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
        if not isinstance(achievement, str):  # Achievement validation
            raise TypeError("Enter a valid achievement. Try again.")
        self.achievement = achievement
        if not isinstance(type, str):  # Type validation
            raise TypeError("Enter a valid type. Try again.")
        self.type = type

    def __repr__(self):
        return f'{self.name}: {self.id}, {self.achievement}, {self.type} '

    def __str__(self):
        return f'<h3>{self.name}: </h3> \
                    <ul>    \
                            <li> ID: {self.id}</li> \
                            <li> Achievement: {self.achievement}</li>   \
                            <li> Type: {self.type}</li> \
                    </ul>'
    
    def from_json(competency_dict):
        if not isinstance(competency_dict,dict):
            raise TypeError("Expected dict")
        return Competency(competency_dict['id'],competency_dict['name'],competency_dict['achievement'],competency_dict['type'])
    
    def to_json(competency):
        if not isinstance(competency,Competency):
            raise TypeError("Expected Address")
        return competency.__dict__
    
class CompetencyForm(FlaskForm):
    id = StringField('Id',validators=
                     [DataRequired(),
                      Regexp('^[0-9A-Z]{4}$', message="Wrong Id format: #### (# => Letter or Digit)")
                      ])
    name = StringField('Name',validators=[DataRequired()])
    achievement = StringField('Achievement',validators=[DataRequired()])
    type = SelectField('Type',validators=[DataRequired()], choices=["Choose Type", "Mandatory", "Optional"])
    
