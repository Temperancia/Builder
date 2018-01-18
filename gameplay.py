class Statistic:
    def __init__(self, name, base_value, growth_value):
        self.name = name
        self.base_value = base_value
        self.growth_value = growth_value
        self.current_value = base_value


class Champion:
    def __init__(self, name, stats):
        self.name = name
        self.statistics = {
            'armor': Statistic('Armor',
                               stats['armor'], stats['armorperlevel']),
            'attackdamage': Statistic('AD',
                                      stats['attackdamage'], stats['attackdamageperlevel']),
            'attackspeed': Statistic('Attack speed',
                                     self.base_attack_speed(stats['attackspeedoffset']), stats['attackspeedperlevel']),
            'hp': Statistic('HP',
                            stats['hp'], stats['hpperlevel']),
            'hpregen': Statistic('HP/s',
                                 stats['hpregen'], stats['hpregenperlevel']),
            'mp': Statistic('MP',
                            stats['mp'], stats['mpperlevel']),
            'mpregen': Statistic('MP/s',
                                 stats['mpregen'], stats['mpregenperlevel'])
        }

    @staticmethod
    def base_attack_speed(offset):
        return 0.625 / (1 + offset)

    def display(self):
        for stat, value in self.statistics.items():
            print(stat + ": " + str(value.base_value))
        print("i display a champion who has " + str(self.statistics['armor'].current_value) + " armor")


class Equipment:
    def __init__(self):
        self.items = ["boots", "etc"]



