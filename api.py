import requests
import json
import collections
import urllib.request


refreshChampions = False
refreshItems = False
params = (
        ('api_key', 'RGAPI-f795ebb7-650a-4de7-ba96-4293ec59360f'),
    )


def __get_data_from_url(url, file_name):
    json_content = requests.get(url, params=params)
    received_file = open(file_name, "wb")
    received_file.write(json_content.content)


def __extract_from_json(file_name):
    json_file = open(file_name, "rb")
    response = json.loads(json_file.read())
    return collections.OrderedDict(sorted(response['data'].items(), key=lambda x: x[1]['name']))


def get_champions():
    file_name = "champions.json"
    if refreshChampions:
        url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?tags=stats&tags=spells'
        __get_data_from_url(url, file_name)
    champions = __extract_from_json(file_name)
    champions['FiddleSticks'] = champions.pop('Fiddlesticks')
    return champions


def get_champion_squares(champions):
    for key, value in champions.items():
        url = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + key + '.png'
        file = 'data/' + key + '.png'
        try:
            urllib.request.urlretrieve(url, file)
        except Exception:
            continue


def get_items():
    file_name = "items.json"
    if refreshItems:
        url = 'https://na1.api.riotgames.com/lol/static-data/v3/items?tags=stats'
        __get_data_from_url(url, file_name)
    return __extract_from_json(file_name)
