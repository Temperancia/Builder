# lets create a parent class for them called Component
# now lets see the point of this parent class


class Component:
    def __init__(self):
        self.totalAttackSpeed = 0

    @staticmethod
    def display():  # in fact , self cannot be omitted BUT when a function does not need
        # any value of the object , whether attribute or method , you can decorate it with AND
        # then ide lets you remove fucking self
        print("i display a component")


class Champion(Component):
    def __init__(self):
        super().__init__()
        self.healthPoints = 100

    def display(self):
        print("i display a champion who has " + str(self.healthPoints) + " HP")


class Runes(Component):
    def __init__(self):
        super().__init__()
        self.effects = "press the attack shit"


class Equipment(Component):
    def __init__(self):
        super().__init__()
        self.items = ["boots", "etc"]



