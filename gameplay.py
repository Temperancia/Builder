class ChampionStatistic:
    def __init__(self, name, base_value, growth_value):
        self.name = name
        self.base_value = base_value
        self.growth_value = growth_value
        self.current_value = base_value
        self.current_factor = 1

    def __iadd__(self, value):
        self.current_value += value
        return self

    def __isub__(self, value):
        self.current_value -= value
        return self

    def __imul__(self, value):
        self.current_value += self.base_value * value
        return self

    def __itruediv__(self, value):
        self.current_value -= self.base_value * value
        return self


class Champion:
    def __init__(self, key, champion=None, level=1):
        self.key = key
        self.level = level
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
                'crit': ChampionStatistic('% Crit',
                                          stats['crit'],
                                          stats['critperlevel']),
                'hp': ChampionStatistic('HP',
                                        stats['hp'],
                                        stats['hpperlevel']),
                'hpregen': ChampionStatistic('HP/s',
                                             stats['hpregen'],
                                             stats['hpregenperlevel']),
                'magicdamage': ChampionStatistic('AP',
                                                 0,
                                                 0),
                'movespeed': ChampionStatistic('MS',
                                               stats['movespeed'],
                                               0),
                'mp': ChampionStatistic('MP',
                                        stats['mp'],
                                        stats['mpperlevel']),
                'mpregen': ChampionStatistic('MP/s',
                                             stats['mpregen'],
                                             stats['mpregenperlevel']),
                'spellblock': ChampionStatistic('MR',
                                                stats['spellblock'],
                                                stats['spellblockperlevel'])
            }
            self.flat_convert_table = {
                'FlatArmorMod': 'armor',
                'FlatPhysicalDamageMod': 'attackdamage',
                'FlatCritChanceMod': 'crit',
                'FlatHPPoolMod': 'hp',
                'FlatMagicDamageMod': 'magicdamage',
                'FlatMovementSpeedMod': 'movespeed',
                'FlatMPPoolMod': 'mp',
                'FlatSpellBlockMod': 'spellblock'
            }
            self.regen_convert_table = {
                'FlatHPRegenMod': 'hpregen',
                'FlatMPRegen': 'mpregen'
            }
            self.percentage_convert_table = {
                'PercentAttackSpeedMod': 'attackspeed'
            }

    @staticmethod
    def base_attack_speed(offset):
        return 0.625 / (1 + offset)

    def set_level(self, level):
        self.level = level
        for key, value in self.statistics.items():
            if key in self.flat_convert_table.values():
                value.current_value += value.growth_value * (self.level - 1)
            elif key in self.percentage_convert_table.values():
                value.current_value += value.base_value * value.growth_value / 100 * (self.level - 1)

    def display(self):
        print(self.name, 'level : ', self.level)
        for stat, value in self.statistics.items():
            print(stat + ': ' + str(value.current_value) + ' ' + value.name)
        print()

    def improve_stat(self, key, value):
        if key in self.flat_convert_table:
            self.statistics[self.flat_convert_table[key]] += value
        elif key in self.regen_convert_table:
            self.statistics[self.regen_convert_table[key]] += value
        elif key in self.percentage_convert_table:
            self.statistics[self.percentage_convert_table[key]] *= value

    def worsen_stat(self, key, value):
        if key in self.flat_convert_table:
            self.statistics[self.flat_convert_table[key]] -= value
        elif key in self.regen_convert_table:
            self.statistics[self.regen_convert_table[key]] -= value
        elif key in self.percentage_convert_table:
            self.statistics[self.percentage_convert_table[key]] /= value

    def update(self, item, improve):
        for key, value in item.stats.items():
            if improve:
                self.improve_stat(key, value)
            else:
                self.worsen_stat(key, value)


class Item:
    def __init__(self, key, item):
        self.key = key
        self.name = item['name']
        self.stats = item['stats']
        self.parse(item['description'])

    def parse(self, description):  # hp regen same issue
        found = description.find('Base Mana Regen')
        if not found == -1:
            self.stats.update({'FlatMPRegen': float(description[found - 4:found - 2])})

    def display(self):
        item = self.name + ': '
        for stat, value in self.stats.items():
            item += stat + ': ' + str(value) + '\t'
        print(item)


class Equipment:
    def __init__(self):
        self.stuff = [None, None, None, None, None, None]

    def reset(self, champion):
        for item in self.stuff:
            if item:
                champion.update(item, True)

    def add_item(self, item, champion):
        for index, x in enumerate(self.stuff):
            if not x:
                self.stuff[index] = item
                if champion:
                    champion.update(item, True)
                return index
        return -1

    def remove_item(self, index, champion):
        if champion:
            champion.update(self.stuff[index], False)
        self.stuff[index] = None

