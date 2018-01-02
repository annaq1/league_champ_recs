from riot_api import *
from riot_logic import *

VALID_REGIONS = {"RU": "ru", "KR": "kr", "BR": "br1", "OCE": "oc1", "JP": "jp1", "NA": "na1",
                  "EUNE": "eun1", "EUW": "euw1", "TR": "tr1", "LAN": "la1", "LAS": "la2"}


def enter_summoner_name():
    """Prompts user to enter summoner name and checks name for validity. If not valid, repeats prompt. Else,
    return summoner name"""
    valid = False
    while not valid:
        summoner_name = input("Please enter your summoner name: ")
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
        region = input("Please enter your region: ").upper()
        if region not in VALID_REGIONS:
            regions = " ".join(x for x in sorted(VALID_REGIONS))
            print("Please enter a valid region. Valid regions: " + regions.strip() + ".")
        else:
            return VALID_REGIONS[region]

     



def user_interface():
    """User interface. Prompts user for summoner name and region. Prints user's current top
    3 champions, and prints 3 suggested champions they might like based on those top 3."""
    print("Hello! Enter your summoner name and region to see your suggested champions.")
    summoner_name = enter_summoner_name()
    region = enter_region()








if __name__ == "__main__":
    user_interface()
    
    
    
