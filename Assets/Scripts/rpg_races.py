''' character race '''
class Race:
    ''' character race '''
    def __init__(self, name, description, abilities):
        self.name = name
        self.description = description
        self.abilities = abilities

    def __str__(self):
        return f"{self.name}: {self.description} | Abilities: {', '.join(self.abilities)}"
    def get():
        pass
