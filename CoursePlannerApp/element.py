
from .competency import Competency

class Element:
    def __init__(self, order, name, criteria, hours, competency):
        if not isinstance(id, order): #Order validation
            raise TypeError("Enter a valid number. Try again.")
        self.order = order
        if not isinstance(name, str): #Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
        if not isinstance(criteria, str): #Criteria validation
            raise TypeError("Enter a valid criteria. Try again.")
        self.criteria = criteria
        if not isinstance(hours, int): #Hours validation 
            raise TypeError("Enter a valid number. Try again.")
        self.hours = hours
        if not isinstance(competency, Competency): #Competency validation 
            raise TypeError("Enter a valid/existing competency. Try again.")
        self.competency = competency
        
    def __repr__(self):
        return f'{self.name}: {self.id}, {self.achievement}, {self.type} '        
     
    def __str__(self): 
        return f'<p>Course {self.name}: {self.id}, {self.achievement}, {self.type} </p>'