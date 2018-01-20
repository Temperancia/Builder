import requests
import json
import collections


refreshChampions = False
refreshItems = False
params = (
        ('api_key', 'RGAPI-728cb974-be95-4525-8abb-c8da7bfa91e1'),
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
    file_name = "rawData.json"
    if refreshChampions:
        url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?tags=stats'
        __get_data_from_url(url, file_name)
    return __extract_from_json(file_name)


def get_items():
    file_name = "items.json"
    if refreshItems:
        url = 'https://na1.api.riotgames.com/lol/static-data/v3/items?tags=stats'
        __get_data_from_url(url, file_name)
    return __extract_from_json(file_name)
