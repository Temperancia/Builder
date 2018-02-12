from gameplay import *
import api
import textwrap


class Build:
    def __init__(self):
        self.champion = None
        self.equipment = Equipment()

        self.champions = api.get_champions()
        self.items, self.tree = api.get_items()
        self.gold = 0

    @staticmethod
    def display_choice(choices):
        output = ''
        for idx, choice in enumerate(choices.values()):
            output += str(idx + 1) + ': ' + choice['name'] + '\t'
        for line in textwrap.wrap(output, 120):
            print(line)

    def __display_build(self):
        print('Current build : ')
        for build_item in self.equipment.stuff:
            build_item.display()

    def select_champion(self):
        names = [champ['name'].lower() for champ in self.champions.values()]
        while True:
            self.display_choice(self.champions)
            selection = input("Select a champion : ")
            if selection.isdigit() and 0 < int(selection) <= len(self.champions):
                index = list(self.champions.keys())[int(selection) - 1]
                break
            elif selection.lower() in names:
                index = list(self.champions.keys())[int(names.index(selection.lower()))]
                break
        self.champion = Champion(self.champions[index])
        while True:
            selection = input("Select a level between 1 and 18 : ")
            if selection.isdigit() and 0 < int(selection) <= 18:
                break
        self.champion.set_level(int(selection))

    def select_items(self):
        names = [item['name'].lower() for item in self.items.values()]
        for iteration in range(6):
            while True:
                self.display_choice(self.items)
                if self.equipment.stuff:
                    self.__display_build()
                selection = input('Select items (separate each by pressing enter) : ')
                if selection.isdigit() and 0 < int(selection) <= len(self.items):
                    index = list(self.items.keys())[int(selection) - 1]
                    break
                elif selection.lower() in names:
                    index = list(self.items.keys())[int(names.index(selection.lower()))]
                    break
            item = self.items[index]
            self.equipment.add_item(item, self.champion)

    # app functions

    def set_champion(self, index):
        self.champion = Champion(index, self.champions[index])
        self.equipment.reset(self.champion)

    def add_item(self, index):
        item = Item(index, self.items[index])
        self.gold += item.gold
        return self.equipment.add_item(item, self.champion)

    def remove_item(self, index):
        item = self.equipment.stuff[index]
        if item:
            self.gold -= item.gold
        self.equipment.remove_item(index, self.champion)