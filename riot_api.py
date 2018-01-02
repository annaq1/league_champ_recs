import urllib.parse
import urllib.request
import json
import re
import pickle
#open_cv: freniel's suggestion

RIOT_API_KEY = "RGAPI-dc2ffb94-4bf8-40ee-a04e-c63ceb78485f" #Expires once a day
BASE_SUMMONER_URL = "https://{}.api.riotgames.com/lol/summoner/v3/summoners/by-name/" #fill in region and name
BASE_CHAMPS_URL = "https://{}.api.riotgames.com/lol/static-data/v3/champions"
BASE_MASTERY_URL = "https://{}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/"


VALID_TAGS = ["all", "allytips", "blurb", "enemytips", "format", "image", "info", 
                  "keys", "lore", "partype", "passive", "recommended",
                  "skins", "spells", "stats", "tags"]


#Define custom exceptions
class InvalidEntryError(Exception): pass #exception to be raised when invalid entry is passed into a build_url function


#build url and get json dictionary

def build_summoner_url(region: str, name: str) -> str:
    """Builds url for summoner object, given summoner name and region."""
    return BASE_SUMMONER_URL.format(region) + urllib.parse.quote(name) + "?" + urllib.parse.urlencode([("api_key", RIOT_API_KEY)])


def build_champion_url(tags = None, region = "na1", data_by_id = False, champ_id = None):
    """Builds url for all champion information. Enter tags in list form for more info about champion.
    If data_by_id is True, returned data will use champion id's as keys. Region doesn't really matter in this case
    so by default it will be na1. If any tags are invalid, raise InvalidEntry exception"""
    #only 10 calls to this allowed per hour. Therefore, save into a file once to cache the data. From there on, only
    #reference the data in that file.
    
    query_parameters = [("locale", "en_US")]
    if tags != None:
        for tag in tags:
            if tag not in VALID_TAGS:
                raise InvalidEntryError("Tag, '{}' entered is invalid".format(tag))
            query_parameters.append(("tags", tag))
    if data_by_id == True:
        query_parameters.append(("dataById", "true"))
    query_parameters.append(("api_key", RIOT_API_KEY))
    if champ_id != None:
        return BASE_CHAMPS_URL.format(region) + "/" + str(champ_id) + "?" + urllib.parse.urlencode(query_parameters)
    return BASE_CHAMPS_URL.format(region) + "?" + urllib.parse.urlencode(query_parameters)


def build_mastery_url(region: str, id: int)-> str:
    """Takes in region as str and summoner id as an integer and returns url for that summoner's total champion mastery"""
    return BASE_MASTERY_URL.format(region) + str(id) + "?" + urllib.parse.urlencode([("api_key", RIOT_API_KEY)])

 
 
    
def build_champion_file():
    """If file exists and contains information, return a dictionary containing that file's info.
     Else, build the file and write information to it. (cache champion data). Therefore, the first time this 
     function is called, it will create the file and return dict. On all subsequent calls, it will use the file to 
     gather the info rather than using the api call, which is limited to 10 per hour. This is fine because 
     the data is static champion data, which only changes once per update of the game."""
    try:
        try:
            with open("champions.txt", "rb") as file:
                champ_dict = pickle.load(file)
            return champ_dict
        except EOFError:
            raise FileNotFoundError
    except FileNotFoundError:
        champ_dict = get_dict(build_champion_url(tags = ["partype", "stats", "tags"]))
        with open("champions.txt", "wb") as file:
            pickle.dump(champ_dict, file)
        return champ_dict





def get_dict(url: str)-> dict:
    """Takes a URL and returns a dict representing the 
    parsed JSON response"""
    response = None
    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')
        
        return json.loads(json_text) #loads converts JSON text to python pbject
    
    finally:
        if response != None: #close response once we are done
            response.close()




if __name__ == "__main__":
    pass
    #champ_dict = build_champion_file()
    #print(champ_dict)
    #url = build_summoner_url("na1", "laslow latte")
    #json_dict = get_dict(url)
    #print(json_dict)
#     champ_url = build_champion_url(tags = ["partype", "stats", "tags"], champ_id = 39)
#     print(champ_url)
#     champ_dict = get_dict(champ_url)
#     print(champ_dict)
    #mastery_url = build_mastery_url("na1", 76782945)
    #mastery_dict = get_dict(mastery_url)
    #print(mastery_url)
    #for item in mastery_dict:
    #    print(item)
    
    
    
    
    
    
    
    
    
    
    