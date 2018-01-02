from riot_api import *
from riot_logic import *

VALID_REGIONS = {"RU": "ru", "KR": "kr", "BR": "br1", "OCE": "oc1", "JP": "jp1", "NA": "na1",
                  "EUNE": "eun1", "EUW": "euw1", "TR": "tr1", "LAN": "la1", "LAS": "la2"}


def enter_summoner_name():
    """Prompts user to enter summoner name and checks name for validity. If not valid, repeats prompt. Else,
    return summoner name"""
    valid = False
    while not valid:
        summoner_name = input("Please enter your summoner name: ").strip()
        pat = re.compile("^(\w|\.|\s)+$")
        valid = pat.match(summoner_name)
        if not valid:
            print("Please enter a valid name. Names can only contain alphanumeric characters, spaces, '_', and '.'")
        else:
            return summoner_name

def enter_region():
    """Prompts user to enter region and checks region for validity. Also converts region to format suitable
    for use in urls and returns"""
    valid = False
    while not valid:
        region = input("Please enter your region: ").upper().strip()
        if region not in VALID_REGIONS:
            regions = " ".join(x for x in sorted(VALID_REGIONS))
            print("Please enter a valid region. Valid regions: " + regions.strip() + ".")
        else:
            return VALID_REGIONS[region]

def recommend(champ_ids: [int]):
    """Prints out recommendations for summoner based on a list of champions"""
    if len(champ_ids) == 0:
        print("Sorry! You do not have enough champion mastery information to generate your recommended champions.")
    for i in range(len(champ_ids)):
        print("Because your #{} champion is {}, you might also enjoy:".format(i+1, CHAMPION_DICT[str(champ_ids[i])]["name"]))
        shared_tags_list = contains_tags(champ_ids[i])
        suggestions = most_similar_champs(str(champ_ids[i]), shared_tags_list)
        if len(suggestions) >= 3:
            for i in range(len(suggestions[:-1])):
                print(CHAMPION_DICT[suggestions[i]]["name"], end = ", ")
            print("and " + CHAMPION_DICT[suggestions[-1]]["name"])
        if len(suggestions) == 2:
            print(CHAMPION_DICT[suggestions[0]]["name"] + " and " + CHAMPION_DICT[suggestions[1]]["name"])
        if len(suggestions) == 1:
            print(CHAMPION_DICT[suggestions[0]]["name"])
        print()
     



def user_interface():
    """Simple user interface. Prompts user for summoner name and region. Prints user's current top
    3 champions, and prints 3 suggested champions they might like based on those top 3."""
    print("Hello! Enter your summoner name and region to see your suggested champions.")
    worked = False
    while not worked:
        try:
            name = enter_summoner_name()
            region = enter_region()
            summoner = Summoner(name, region)
            top3 = summoner.top_three #need to account for if this number is 0
            worked = True
        except urllib.error.HTTPError:
            print("That summoner does not exist for this region. Please try again.")
    print()
    recommend(top3)
    
    



if __name__ == "__main__":
    user_interface()
    
    
    
