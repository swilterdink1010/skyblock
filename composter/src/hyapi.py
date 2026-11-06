import requests, os, time
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
if not HYPIXEL_API_KEY:
    raise RuntimeError("HYPIXEL_API_KEY is not set")
HEADERS = {
    "API-Key": HYPIXEL_API_KEY,
}

def get_uuid(username: str) -> str:
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    if response.status_code == 200:
        return response.json()["id"]
    else: raise RuntimeError(f"Could not get UUID <{response.status_code}> [{response.content}]")
    
    
def get_profiles(uuid: str) -> dict:
    response = requests.get("https://api.hypixel.net/v2/skyblock/profiles", headers=HEADERS, params={"uuid": uuid})
    if response.status_code == 200:
        return response.json()["profiles"]
    else: raise RuntimeError(f"Could not get profile data <{response.status_code}> [{response.content}]")
    
    
def get_profile_id(profile_name: str, uuid: str, profiles: dict | None = None) -> str:
    if profiles is None:
        profiles = get_profiles(uuid)
    for profile in profiles:
        if profile["cute_name"].lower() == profile_name.lower():
            return profile["profile_id"]
    raise KeyError(f"Could not find profile {profile_name} in user profiles")


def get_garden_data(profile_id: str) -> dict:
    response = requests.get("https://api.hypixel.net/v2/skyblock/garden", headers=HEADERS, params={"profile": profile_id})
    if response.status_code == 200:
        return response.json()["garden"]
    else: raise RuntimeError(f"Could not get garden data <{response.status_code}> [{response.content}]")

BuyMode = Literal["instant", "order"]
SellMode = Literal["instant", "offer"]
PriceField = Literal["buyPrice", "sellPrice"]

BUY_PRICE_FIELD: dict[BuyMode, PriceField] = {
    "instant": "buyPrice",
    "order": "sellPrice",
}
BUY_MODE_LABELS: dict[BuyMode, str] = {
    "instant": "Instant Buy", 
    "order": "Buy Order"
}

SELL_MODE_LABELS: dict[SellMode, str] = {
    "instant": "Instant Sell", 
    "offer": "Sell Offer"
}
SELL_PRICE_FIELD: dict[SellMode, PriceField] = {
    "instant": "sellPrice",
    "offer": "buyPrice",
}

_bz_cache = {
    "timestamp": float("-inf"),
    "data": {},
}
def get_bz_data(data_lifetime: int = 300) -> dict:
    if time.monotonic() - _bz_cache["timestamp"] >= data_lifetime:
        response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar", headers=HEADERS)
        if response.status_code == 200:
            _bz_cache["timestamp"] = time.monotonic()
            _bz_cache["data"] = response.json()["products"]
        else: raise RuntimeError(f"Could not get bazaar data <{response.status_code}> [{response.content}]")
    return _bz_cache["data"]


def get_bz_price(id: str, field: Literal["buyPrice", "sellPrice"] = "buyPrice") -> float:
    if not get_bz_data().get(id):
        raise KeyError(f"Invalid input: {id}")
    return get_bz_data()[id]["quick_status"][field]


def main() -> None:
    pass
    
if __name__ == "__main__":
    main()