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


# does not contain rakan xayah ornn kayn zoe squares as most recent , although sknins and splasharts are available ...
def get_champion_squares(champions):
    for key, value in champions.items():
        url = 'http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/' + key + '.png'  # getting each
        # champion with url
        file = 'data/' + key + '.png'  # local file
        try:  # exceptions allow us to handle if something goes wrong easily , it's a rather dumb way to prevent
            # errors but it works often that way in python
            urllib.request.urlretrieve(url, file)  # actual retrieving if not 404 or 403 + stores into local file
        except Exception:
            continue  # if goes wrong , still continue the loop above , aka goes next iteration , "next" in other
            # languages


def get_items():
    file_name = 'items.json'
    if refreshItems:
        url = 'https://na1.api.riotgames.com/lol/static-data/v3/items?tags=stats'
        __get_data_from_url(url, file_name)
    return __extract_from_json(file_name)
