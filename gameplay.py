class Statistic:
    def __init__(self, name, base_value):
        self.name = name
        self.base_value = base_value


class ChampionStatistic(Statistic):
    def __init__(self, name, base_value, growth_value):
        super().__init__(name, base_value)
        self.growth_value = growth_value
        self.current_value = base_value

    def __iadd__(self, value):
        self.current_value += value
        return self

class ItemStatistic(Statistic):
    def __init__(self, name, base_value):
        super().__init__(name, base_value)


class Champion:
    def __init__(self, champion=None):
        if champion:
            self.name = champion['name']
            stats = champion['stats']
            self.statistics = {
                'armor': ChampionStatistic('Armor',
                                           stats['armor'],
                                           stats['armorperlevel']),
                'attackdamage': ChampionStatistic('AD',
                                                  stats['attackdamage'],
                                                  stats['attackdamageperlevel']),
                'attackspeed': ChampionStatistic('Attack speed',
                                                 self.base_attack_speed(stats['attackspeedoffset']),
                                                 stats['attackspeedperlevel']),
                'hp': ChampionStatistic('HP',
                                        stats['hp'],
                                        stats['hpperlevel']),
                'hpregen': ChampionStatistic('HP/s',
                                             stats['hpregen'],
                                             stats['hpregenperlevel']),
                'movespeed': ChampionStatistic('MS',
                                               stats['movespeed'],
                                               0),
                'mp': ChampionStatistic('MP',
                                        stats['mp'],
                                        stats['mpperlevel']),
                'mpregen': ChampionStatistic('MP/s',
                                             stats['mpregen'],
                                             stats['mpregenperlevel'])
            }

    @staticmethod
    def base_attack_speed(offset):
        return 0.625 / (1 + offset)

    def display(self):
        for stat, value in self.statistics.items():
            print(stat + ": " + str(value.current_value))

    def improve_stat(self, key, value):
        if key == 'FlatArmorMod':
            print(key, value)
            self.statistics['armor'] += value

    def update(self, item):
        # self.display()
        for key, value in item['stats'].items():
            self.improve_stat(key, value)
        self.display()


class Item:
    def __init__(self, name, stats):
        self.name = name
        print(stats)

    def display(self):
        for stat, value in self.statistics.items():
            print(stat + ": " + str(value.base_value))

    def update(self):
        pass


class Equipment:
    def __init__(self):
        self.stuff = []
        # initiate a list of 6 None , will be our stuff we choose
        # find on riot api the list of all the items , use my query in main.py
        # make a function get_items() in main.py that will return you a dictionary of all the items
        # quite similar to get_champions()

        # make a new class "Item" which will encapsulate data from the dict like the "Statistic" class above
        # so we can access them easily. Item class must contain ALL statistics so we will simply add all of them
        # when we select an item in a generic way. Use the same statistics dictionary attribute to store them.
        # constructor takes item dictionary
        # eg of final usage : print(self.items['Void Staff'].statistics['armor'])
        # or => item = self.items['Void Staff']
        # print(item.statistics['armor'])

        # make regularly tests with print to check data access and integrity

        # make a function inside this class "add_item(item)" which adds item to the list
        # of items here
        # make a function "remove_item(name)" which will remove from the list of items the last item
        # which has the given name

        # update champion class by making function "update_equipment(equipment)" where you send
        # an Equipment object and then modify current_value of each statistic thanks to each item stats

        # we want our build to be shared between champions possibly so it means Equipment will be
        # outside champion class and imported into each time we need to change stats via : add_item,
        # remove_item
    def add_item(self, item):
        self.stuff.add(Item(item['name'], item['stats']))

