from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class Domain:
    def __init__(self, id, name, description):
        if not isinstance(id, int):  # Id validation
            raise TypeError("Enter a valid id. Try again.")
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
    id = IntegerField('Id',validators=[DataRequired(),
                                        NumberRange(min=1)])
    name = StringField('Name',validators=[DataRequired()])
    description = StringField('Domain Description',validators=[DataRequired()])
