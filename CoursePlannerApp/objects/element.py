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
        return f'<p>Element {self.name}: {self.id}, {self.order}, {self.criteria}, {self.competencyId} </p>'
