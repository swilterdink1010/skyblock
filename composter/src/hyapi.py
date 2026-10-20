import requests, os

from dotenv import load_dotenv
load_dotenv()

HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
HEADERS = {
    "API-Key": HYPIXEL_API_KEY,
}

def get_uuid(username: str):
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if response.status_code == 200:
        return response.json()["id"]
    else: raise RuntimeError(f"Could not get UUID <{response.status_code}> [{response.content}]")
    
    
def get_profiles(uuid: str):
    response = requests.get("https://api.hypixel.net/v2/skyblock/profiles", headers=HEADERS, params={"uuid": uuid})
    if response.status_code == 200:
        return response.json()["profiles"]
    else: raise RuntimeError(f"Could not get profile data <{response.status_code}> [{response.content}]")
    
    
def get_profile_id(profile_name: str, uuid: str, profiles: dict = None): # type: ignore
    if profiles is None:
        profiles = get_profiles(uuid)
    for profile in profiles:
        if profile["cute_name"].lower() == profile_name.lower():
            return profile["profile_id"]
    raise KeyError(f"Could not find profile {profile_name} in user profiles")


def get_garden_data(profile_id: str):
    response = requests.get("https://api.hypixel.net/v2/skyblock/garden", headers=HEADERS, params={"profile": profile_id})
    if response.status_code == 200:
        return response.json()["garden"]
    else: raise RuntimeError(f"Could not get garden data <{response.status_code}> [{response.content}]")


def get_bz_data():
    response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar", headers=HEADERS)
    if response.status_code == 200:
        return response.json()["products"]
    else: raise RuntimeError(f"Could not get garden data <{response.status_code}> [{response.content}]")


def main():
    uuid = get_uuid("bigman7305")
    profile = get_profile_id("Peach", uuid)
    print(get_garden_data(profile)["composter_data"]["upgrades"])
    
    
if __name__ == "__main__":
    main()