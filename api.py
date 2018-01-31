import requests
import json
import collections
import urllib.request


refreshChampions = False
refreshItems = False
params = (
        ('api_key', 'RGAPI-711f59c8-08f8-46a7-a84c-057057c42163'),
    )


def __get_data_from_url(url, file_name):
    json_content = requests.get(url, params=params)
    received_file = open(file_name, 'wb')
    received_file.write(json_content.content)


def __extract_from_json(file_name):
    json_file = open(file_name, 'rb')
    response = json.loads(json_file.read())
    return collections.OrderedDict(sorted(response['data'].items(), key=lambda x: x[1]['name']))


def get_champions():
    file_name = 'champions.json'
    if refreshChampions:
        url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?tags=stats&tags=spells'
        __get_data_from_url(url, file_name)
    champions = __extract_from_json(file_name)
    champions['FiddleSticks'] = champions.pop('Fiddlesticks')  # interesting wrong key for fiddlesticks
    # known issue from api
    return champions


def get_champion_squares(champions):
    for key in champions.keys():
        url = 'http://ddragon.leagueoflegends.com/cdn/8.2.1/img/champion/' + key + '.png'
        file = 'data/champion_squares/' + key + '.png'
        try:
            urllib.request.urlretrieve(url, file)
        except Exception:
            continue


def get_champion_loading_splash_arts(champions):
    for key in champions.keys():
        url = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/' + key + '_0.jpg'
        file = 'data/loading_splash_arts/' + key + '.jpg'
        try:
            urllib.request.urlretrieve(url, file)
        except Exception:
            continue


def get_items():
    file_name = 'items.json'
    if refreshItems:
        url = 'https://na1.api.riotgames.com/lol/static-data/v3/items?tags=stats'
        __get_data_from_url(url, file_name)
    return __extract_from_json(file_name)


def get_items_squares(items):
    for key in items.keys():
        url = 'http://ddragon.leagueoflegends.com/cdn/8.2.1/img/item/' + key + '.png'
        file = 'data/item_squares/' + key + '.png'
        try:
            urllib.request.urlretrieve(url, file)
        except Exception:
            continue
