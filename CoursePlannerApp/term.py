class Term:
    def __init__(self, id, name):
        if not isinstance(id, int): #Id validation
            raise TypeError("Enter a valid id. Try again.")
        self.id = id
        if not isinstance(name, str): #Name validation
            raise TypeError("Enter a valid name. Try again.")
        self.name = name
                
    def __repr__(self):
        return f'{self.name}: {self.id}'        
     
    def __str__(self): 
        return f'<p>Term {self.name}: {self.id}</p>'