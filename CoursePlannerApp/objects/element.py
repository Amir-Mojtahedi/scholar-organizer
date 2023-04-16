from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class Element:
    def __init__(self, id, order, name, criteria, competencyId):
        if not isinstance(id, int): #Id validation 
            raise TypeError("Enter a valid number. Try again.")
        self.id = id
        if not isinstance(order, int): #Order validation
            raise TypeError("Enter a valid number. Try again.")
        self.order = order
        if not isinstance(name, str): #Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
        if not isinstance(criteria, str): #Criteria validation
            raise TypeError("Enter a valid criteria. Try again.")
        self.criteria = criteria
        if not isinstance(competencyId, str): #Competency validation 
            raise TypeError("Enter a the Id of a valid/existing competency. Try again.")
        self.competencyId = competencyId
        
    def __repr__(self):
        return f'{self.name}: {self.id}, {self.order}, {self.criteria}, {self.competencyId}'        
     
    def __str__(self): 
        return f'<h3>{self.name} </h3> \
                    <ul>    \
                            <li> ID: {self.id}</li> \
                            <li> Order: {self.order}</li>   \
                            <li> Criteria: {self.criteria}</li> \
                            <li> Competency ID: {self.competencyId}</li>    \
                    </ul>'

class ElementForm(FlaskForm):
    id = IntegerField('Id',validators=
                                [DataRequired(), 
                                 NumberRange(min=1)
                                 ])
    order = IntegerField('Order',validators=
                                [DataRequired(), 
                                 NumberRange(min=1)
                                 ])
    name = StringField('Name',validators=[DataRequired()])
    criteria = StringField('Criteria',validators=[DataRequired()])
    competencyId = SelectField('Id of associated Competency',validators=[DataRequired()], choices=[])
