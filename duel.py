from gameplay import *
import api
import build
import schedule


class Duel:
    def __init__(self):

        self.time = 0

        self.champions = api.get_champions()

        self.first_champion = self.select_champion()
        self.second_champion = self.select_champion()

        self.duel()

    def select_champion(self):
        names = [champ['name'].lower() for champ in self.champions.values()]
        while True:
            build.Build.display_choice(self.champions)
            selection = input('Select a champion : ')
            if selection.isdigit() and 0 < int(selection) <= len(self.champions):
                index = list(self.champions.keys())[int(selection) - 1]
                break
            elif selection.lower() in names:
                index = list(self.champions.keys())[int(names.index(selection.lower()))]
                break
        return Champion(self.champions[index])
        # self.champion = Champion(self.champions[index])
        # while True:
        #     selection = input('Select a level between 1 and 18 : ')
        #     if selection.isdigit() and 0 < int(selection) <= 18:
        #         break
        # self.champion.set_level(int(selection))

    # here it's the start of the duel as you may have understood , we're about to launch a schedule object
    # which will each millisecond run the tick function to emulate 2 champions AA-ing
    def duel(self):
        schedule.every(0.001).seconds.do(self.tick)
        while True:
            schedule.run_pending()

    # if we increase the tick which is the number of milliseconds since the duel has started
    # directly, we will skip the first auto when it starts and indeed we didnt get first auto
    # now it works but there is another mistake you may have noticed, have you ?
    def tick(self):
        if self.time % int(1 / self.first_champion.statistics['attackspeed'].current_value * 1000) == 0:
            print('t=', self.time, ':', self.first_champion.name, 'attacks')
        if self.time % int(1 / self.second_champion.statistics['attackspeed'].current_value * 1000) == 0:
            print('t=', self.time, ':', self.second_champion.name, 'attacks')
        self.time += 1
