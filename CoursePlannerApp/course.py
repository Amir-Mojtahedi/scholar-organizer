from .term import Term
from .domain import Domain


class Course:
    def __init__(self, id, name, description, term, domain, lab_hours, theory_hours, work_hours):
        if not isinstance(id, int): #Number validation
            raise TypeError("Enter a valid number. Try again.")
        self.id = id
        if not isinstance(name, str): #Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
        if not isinstance(description, str): #Description validation
            raise TypeError("Enter a valid Description. Try again.")
        self.description = description
        if not isinstance(term, Term): #Term validation (Takes an actual term object)
            raise TypeError("Enter a valid/existing Term. Try again.")
        self.term = term
        if not isinstance(domain, Domain): #Description validation (Takes an actual domain object)
            raise TypeError("Enter a valid/existing Domain. Try again.")
        self.domain = domain
        if not isinstance(lab_hours, str): #Lab hours validation
            raise TypeError("Enter a valid format for lab hours. Try again.")
        self.lab_hours = lab_hours
        if not isinstance(theory_hours, str): #Theory Hours validation
            raise TypeError("Enter a valid format for theory hours. Try again.")
        self.theory_hours = theory_hours
        if not isinstance(work_hours, str): #Work Hours validation
            raise TypeError("Enter a valid format for work hours. Try again.")
        self.work_hours = work_hours
        
    def __repr__(self):
        return f'{self.name}: {self.id}, {self.description}, {self.term}, {self.domain}, {self.lab_hours}, {self.theory_hours}, {self.work_hours} '        
     
    def __str__(self): 
        return f'<p>Course {self.name}: {self.id}, {self.description}, {self.term}, {self.domain}, {self.lab_hours}, {self.theory_hours}, {self.work_hours} </p>'