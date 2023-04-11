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
        return f'<p>Competency {self.name}: {self.id}, {self.achievement}, {self.type} </p>'
