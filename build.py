from gameplay import *
#cool!
# this was raw code without any architecture now we need to think about an actual structure for
# our application
# lets think about a "build" , something you choose with 3 things : a champion , a set of runes
# and finally the items
# we simply make 3 objects from classes we will further describe , in bigger projects
# this conception phase is performed using UML to model relationships between classes
# we are about to see inheritance that way
# lets say that each of "build" is a "Component"
class Build:
    def __init__(self):
        self.champion = Champion()
        self.runes = Runes()
        self.equipment = Equipment()s

build = Build()
print(build.champion.healthPoints)
print(build.champion.totalAttackSpeed)
print(build.equipment.items[0])
print(build.equipment.totalAttackSpeed)
print(build.runes.effects)
print(build.runes.totalAttackSpeed)
build.equipment.display()
build.champion.display()
