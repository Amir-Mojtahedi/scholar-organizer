class Course:
    def __init__(self, id, name, description, termId, domainId, lab_hours, theory_hours, work_hours):
        if not isinstance(id, str): #Number validation
            raise TypeError("Enter a valid number. Try again.")
        self.id = id
        if not isinstance(name, str): #Name validation
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
        if not isinstance(termId, int): #Term validation 
            raise TypeError("Enter a valid/existing Term ID. Try again.")
        self.termId = termId
        if not isinstance(domainId, int): #Domain validation
            raise TypeError("Enter a valid/existing Domain ID. Try again.")
        self.domainId = domainId

        
    def __repr__(self):
        return f'{self.name}: {self.id}, {self.description}, {self.termId}, {self.domainId}, {self.lab_hours}, {self.theory_hours}, {self.work_hours} '        
     
    def __str__(self): 
        return f'<p>Course {self.name}: {self.id}, {self.description}, {self.termId}, {self.domainId}, {self.lab_hours}, {self.theory_hours}, {self.work_hours} </p>'