#Make class or namedtuple for summoner name
#potential info to return:
#number of hours spent playing league in the last week !!!
#most played champ of all time (mastery)
#most played champ in last 20 games
#rank
#winrate on certain champs


###Recommended champions based on the player's most-played champions
"""Algorithm:
    1. Return top 3 champions based on mastery points (or 1 if 3 is too difficult) *
    2. Make a list of champions with same tags as given champion
    3. Make a list of champions with same tags as 3 champions
    4. Sort list by number of most common attributes (recommended item build?)
    5. Find top 3 champions on that list
    6. Return 3 recommended champions for the person to play
    6.5 Alternatively, do this per champion instead of combining the 3. Trial and error to see which method is better
"""

from riot_api import *
    
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
    
    
# Sadly doesn't work because it limits to 10 requests per hour. Change it so that I write all the champion data to a file
# and then use that file in order to get the information.
# class Champion:
#     def __init__(self, champ_id: int):
#         champ_url = build_champion_url(tags = ["partype", "stats", "tags"], champ_id = champ_id)
#         champ_dict = get_dict(champ_url)
#         print(champ_dict)
#         
#         self.id = champ_id
#         self.name = champ_dict["name"]     
#         self.tags = champ_dict["tags"]
#         self.partype = champ_dict["partype"]
#         self.armor = champ_dict["stats"]["armor"]
#         self.attack_damage = champ_dict["stats"]["attackdamage"]
#         self.attack_range = champ_dict["stats"]["attackrange"]
#         self.hp = champ_dict["stats"]["hp"]
#         self.mp = champ_dict["stats"]["mp"]


def contains_tags(champ: str) -> [int]:
    """Returns list of champions that has at least one tag in common with the given champion"""
    



    
        


if __name__ == "__main__":
    s1 = Summoner("laslow latte", "na1")
    print(s1.name, s1.summoner_level)
    print(s1.id)
    print(s1.top_three)
    print(CHAMPION_DICT)
        