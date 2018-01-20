from gameplay import *
import api
import textwrap


class Build:
    def __init__(self):
        self.champion = Champion()
        self.equipment = Equipment()

        self.champions = api.get_champions()
        self.items = api.get_items()

        self.select_champion()
        self.select_items()

    def display_choice(self, choices):
        output = ''
        for idx, choice in enumerate(choices.values()):
            output += str(idx + 1) + ': ' + choice['name'] + '\t'
        for line in textwrap.wrap(output, 120):
            print(line)

    def select_champion(self):
        names = [champ['name'].lower() for champ in self.champions.values()]
        while True:
            # self.display_choice(self.champions)
            selection = input("Select a champion : ")
            if selection.isdigit() and 0 < int(selection) <= len(self.champions):
                index = list(self.champions.keys())[int(selection) - 1]
                break
            elif selection.lower() in names:
                index = list(self.champions.keys())[int(names.index(selection.lower()))]
                break
        self.champion = Champion(self.champions[index])

    def select_items(self):
        names = [item['name'].lower() for item in self.items.values()]
        for iteration in range(6):
            while True:
                # self.display_choice(self.items)
                if self.equipment.stuff:
                    print('Current build : ')
                    for build_item in self.equipment.stuff:
                        print('\t' + build_item['name'])
                selection = input('Select items (separate each by pressing enter) : ')
                if selection.isdigit() and 0 < int(selection) <= len(self.items):
                    index = list(self.items.keys())[int(selection) - 1]
                    break
                elif selection.lower() in names:
                    index = list(self.items.keys())[int(names.index(selection.lower()))]
                    break
            item = self.items[index]
            self.equipment.stuff.append(item)
            self.champion.update(item)
