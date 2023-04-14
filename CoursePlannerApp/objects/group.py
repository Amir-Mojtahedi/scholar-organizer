class Group:
    def __init__(self, name, id=None):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if id and not isinstance(id, int):
            raise TypeError("Id must be an integer")

        self.name = name
        self.id = id

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"
