import requests
import json
import collections

import gameplay


def get_champions():
    params = (
        ('api_key', 'RGAPI-a978ebd8-1ab1-4785-9da5-d375977e485b'),
    )
    url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?tags=stats'
    # jsonContent = requests.get(url, params=params)
    # receivedFile = open("rawData.json", "wb")
    # receivedFile.write(jsonContent.content)

    json_file = open("rawData.json", "rb")
    response = json.loads(json_file.read())
    return collections.OrderedDict(sorted(response['data'].items(), key=lambda x: x[1]['name']))


def display_all_stats():
    for champion, attributes in champions.items():
        print(champion)
        for key, value in attributes.items():
            if isinstance(value, dict):
                print("\tstats :")
                for stat, stat_value in value.items():
                    print("\t\t%s : %s" % (stat, stat_value))
            else:
                print("\t%s : %s" % (key, value))


def greetings():
    print("Hello toxic player.")


def select_champion():
    names = [champ['name'].lower() for champ in champions.values()]
    while True:
        for idx, (key, champ) in enumerate(champions.items()):
            print(str(idx + 1) + ": " + champ['name'])
        champion = input("Select a champion : ")
        if champion.isdigit() and 0 < int(champion) <= len(champions):
            champion = list(champions.keys())[int(champion) - 1]
            break
        elif champion.lower() in names:
            champion = list(champions.keys())[int(names.index(champion.lower()))]
            break
    return champions[champion]


if __name__ == '__main__':
    greetings()
    champions = get_champions()
    champion = select_champion()
    #display_all_stats()
    gameplay.Champion(champion['name'], champion['stats']).display()

