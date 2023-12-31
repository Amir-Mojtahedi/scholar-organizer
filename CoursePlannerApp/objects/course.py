from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, Regexp, NumberRange

class Course:
    def __init__(self, id, name, description, termId, domainId, lab_hours, theory_hours, work_hours):
        if not isinstance(id, str): #Id validation
            raise TypeError("Enter a valid Id. Try again.")
        self.id = id
        if not isinstance(name, str):  # Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
        if not isinstance(theory_hours, int): #Theory Hours validation
            raise TypeError("Enter a valid format for theory hours. Try again.")
        self.theory_hours = theory_hours
        if not isinstance(lab_hours, int): #Lab hours validation
            raise TypeError("Enter a valid format for lab hours. Try again.")
        self.lab_hours = lab_hours
        if not isinstance(work_hours, int): #Work Hours validation
            raise TypeError("Enter a valid format for work hours. Try again.")
        self.work_hours = work_hours
        if not isinstance(description, str): #Description validation
            raise TypeError("Enter a valid Description. Try again.")
        self.description = description
        # if termId.isdigit(): 
        #     termId = int(termId) 
        # if not isinstance(termId, int): #Term validation 
        #     raise TypeError("Enter a valid/existing Term ID. Try again.")
        self.termId = termId
        # if domainId.isdigit(): 
        #     domainId = int(domainId) 
        # if not isinstance(domainId, int): #Domain validation
        #     raise TypeError("Enter a valid/existing Domain ID. Try again.")
        self.domainId = domainId
       
    def __repr__(self):
        return f'{self.name}: {self.id}, {self.description}, {self.termId}, {self.domainId}, {self.lab_hours}, {self.theory_hours}, {self.work_hours} '        
     
    def __str__(self): 
        return f'<h3>{self.name}: </h3> \
                    <ul>    \
                            <li> ID: {self.id}</li> \
                            <li> Description: {self.description}</li>   \
                            <li> Term ID: {self.termId}</li> \
                            <li> Domain ID: {self.domainId}</li>    \
                            <li> Lab Hours: {self.lab_hours}</li>   \
                            <li> Theory Hours: {self.theory_hours}</li> \
                            <li> Work Hours: {self.work_hours} </li>    \
                    </ul>'
    
class CourseForm(FlaskForm):
    
    id = StringField('Id', validators=
                     [DataRequired(),
                      Regexp('^[0-9A-Z]{3}-[0-9A-Z]{3}-[0-9A-Z]{2}$', message="Wrong Id format: ###-###-## (# => Letter or Digit)")
                      ])
    name = StringField('Name',validators=
                       [DataRequired(), 
                        Regexp('^[A-Za-z\s]*', message=" Wrong Name format (Only letters)")])
    theory_hours = IntegerField('Theory Hours',validators=
                                [DataRequired(), 
                                 NumberRange(min=1, max=5)
                                 ])
    lab_hours = IntegerField('Lab Hours',validators=
                                [DataRequired(), 
                                 NumberRange(min=1, max=5)
                                 ])
    work_hours = IntegerField('Work Hours',validators=
                                [DataRequired(), 
                                 NumberRange(min=1, max=5)
                                 ])
    description = StringField('Course Description',validators=[DataRequired()])
    
    termId = SelectField('Id of associated Term',validators=[DataRequired()], choices=[])
    domainId = SelectField('Id of associated Domain',validators=[DataRequired()], choices=[])
