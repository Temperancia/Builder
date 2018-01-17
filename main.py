import requests #  module i installed via settings : allows me to use get http function to retrieve
# data from LOL api via an url and an api key
import json
import collections
params = (
    ('api_key', 'RGAPI-a978ebd8-1ab1-4785-9da5-d375977e485b'),
)  # notice a tuple

# here i get a response in json which is a very famous data type (along xml)
# syntax is like [{ { , }}]
# i decode json via json native python module function loads which takes the json and returns
# an actual pythonic list
# tried retarded query and burnt quota i hope it's back
#jsonContent = requests.get('https://na1.api.riotgames.com/lol/static-data/v3/champions?tags=stats', params=params)
#receivedFile = open("rawData.json", "wb")
#receivedFile.write(jsonContent.content)

# moral of the story : never assume a solution like converting bytes to string , error told
# me i was writing bytes on that , casted instead of using appropriate solution
jsonFile = open("rawData.json", "rb")  # reading rights this time right
# write opening has erased somehow : /
content = jsonFile.read()
response = json.loads(content)

data = response['data']
# as i have told you there is very limited rate 10/h requests from the api
# so here we are going to store the data inside a local file ok ? i need you to understand fully
# everything above until now so i can actually code as i would rn
# good
# actually lets do something better instead of burning each request


def display_all_stats(data):
    # here we open a file in our current directory with write rights
    for champion in data:  # for each item we will write the value but we need to do that for each
        print(champion)
        for key in data[champion]:
            value = str(data[champion][key])
            print("\t%s : %s" % (key, value))  # right cant iterate on a value
# \t is a tabulation , in ascii i dont remember ...
# \n is a carriage return , in ascii = 10
# well a good first shot 9 remaining though

# we will need to lower both values i think when checking
# this is becoming chaotic lets make functions


def greetings(data):
    print("Hello toxic player.")


def base_attack_speed(offset):
    return 0.625 / (1 + offset)



def select_champion(champions):
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

    print(champions[champion])
    print(base_attack_speed(champions[champion]['stats']['attackspeedoffset']))
# we have first to sort data alphabetically
# this hardcore syntax is a lambda function within a sort call, this makes our sorting custom
# we use name attribute of each iteration on our dictionary, the iterator is k
# with lower level languages you will understand this mechanic better for now just trust it
new_data = collections.OrderedDict(sorted(data.items(), key=lambda x: x[1]['name']))  # this works lol

greetings(new_data)
select_champion(new_data)
#display_all_stats(data)

# here i have typical problem : i want a fully ordered dictionary which i cant have without some
# hard code when i could simply display the list i've got and make a workaround without input

