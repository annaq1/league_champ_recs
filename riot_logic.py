###Recommended champions based on the player's most-played champions
"""Algorithm:
    1. Return top 3 champions based on mastery points
    2. Make a list of champions with same tags as given champion
    3. Sort list by number of common attributes
    4. Return list containing only champions with top # of shared attributes, including ties
    5. Print recommended champions for the person to play, based on their top 3 champions
"""

from riot_api import *
from collections import defaultdict
    
CHAMPION_DICT = build_champion_file()["data"]


class Summoner:
    def __init__(self, name: str, region: str):
        url = build_summoner_url(region, name)
        json_dict = get_dict(url)
        
        self.region = region
        self.id = json_dict["id"]
        self.name = json_dict["name"]
        self.summoner_level = json_dict["summonerLevel"]
        self.profile_icon_id = json_dict["profileIconId"]
        self.account_id = json_dict["accountId"]
        self.revision_date = json_dict["revisionDate"]
        self.top_three = self.top_three()
    
    def top_three(self) -> [int]:
        """Returns top 3 champions that the summoner plays, based on number of mastery points.
        If they have no mastery points on any champion, return empty list. If they have less than 3 champions
        with mastery points, return a list with that number of champions (1 or 2). Champions will
        be identified by an integer representing champion ID, not by name"""
        
        mastery_url = build_mastery_url(self.region, self.id)
        #mastery_list is already sorted, from largest to smallest championPoints number
        mastery_list = get_dict(mastery_url) #returns a list of dictionaries with champion mastery information 
        if len(mastery_list) == 0:
            return []
        if len(mastery_list) < 3:
            return [x["championId"] for x in mastery_list]
        return [x["championId"] for x in mastery_list[:3]]
        
    #possible future projects
    #def match_time(self): #returns time spent in past week on league
    #def most_played(self): #returns most-played champion in past week
    
    

def contains_tags(champ_id: int) -> {str}:
    """Returns set of champions that has at least one tag in common with the given champion,
    but excluding the given champion"""
    same_tags = set()
    champ_info = CHAMPION_DICT[str(champ_id)] #dictionary of information of champion
    champ_tags = champ_info["tags"]
    for c, c_info in CHAMPION_DICT.items():
        if c != str(champ_id): #excludes the given champion
            for tag in champ_tags:
                if tag in c_info["tags"]:
                    same_tags.add(c)
    return same_tags



def number_similarities(id1: str, id2: str) -> int:
    """Compares 2 champions and returns a number: the number of similarities the stats of id2 has with id1.
    1. Checks attackrange. If they are within 25 range of each other, add 3 points
    2. Checks armor. If they are within 10 armor of each other, add 2 points
    3. Checks hp. If they are within 20 range of each other, add 1 point
    4. Checks mp. If it is within 50 range of each other, add 1 point
    5. Checks movespeed. If it is within 5 range of each other, add 1 point
    6. Checks tags. If both tags match, add 2 points
    7. Checks partype. If it matches, add 1 point
    """
    num = 0
    info1 = CHAMPION_DICT[id1]["stats"]
    info2 = CHAMPION_DICT[id2]["stats"]
    if abs(info1["attackrange"] - info2["attackrange"]) <= 25: num +=3 #1
    if abs(info1["armor"] - info2["armor"]) <= 10: num +=2 #2
    if abs(info1["hp"] - info2["hp"]) <=20: num +=1 #3
    if abs(info1["mp"] - info2["mp"]) <=50: num +=1 #4
    if abs(info1["movespeed"] - info2["movespeed"]) <=5: num +=1 #5    
    if CHAMPION_DICT[id1]["tags"] == CHAMPION_DICT[id2]["tags"]: num +=1 #6
    if CHAMPION_DICT[id1]["partype"] == CHAMPION_DICT[id2]["partype"]: num += 1 #7
    return num



def most_similar_champs(champ_id: str, champ_list: [str]) ->[str]:
    """Takes champion id and list of champions and returns a list of champion id's that correspond to the 
    max number calculated in number_similarities. Champ_list is list returned from contains_tags"""
    D = defaultdict(list)
    for champ in champ_list:
        D[number_similarities(champ_id, champ)].append(champ)
    return D[sorted(dict(D), reverse = True)[0]]


    
    
