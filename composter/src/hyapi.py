import requests, os, time, threading
from typing import Literal
from dotenv import load_dotenv

load_dotenv()
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
if not HYPIXEL_API_KEY:
    raise RuntimeError("HYPIXEL_API_KEY is not set")
HEADERS = {
    "API-Key": HYPIXEL_API_KEY,
}

_uuid_cache = {}
UUID_CACHE_LIMIT = 4096
def _drop_uuid_cache() -> None:
    oldest = min(_uuid_cache, key=lambda x: _uuid_cache[x]["timestamp"])
    del _uuid_cache[oldest]
    
def get_uuid(username: str, data_lifetime: int = 86400) -> str:
    username = username.lower()
    if username not in _uuid_cache:
        _uuid_cache[username] = {
            "timestamp": float("-inf"),
            "uuid": "",
        }
    if time.monotonic()-_uuid_cache[username]["timestamp"] >= data_lifetime:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}", timeout=10)
        if response.status_code == 200:
            _uuid_cache[username]["uuid"] = response.json()["id"]
            _uuid_cache[username]["timestamp"] = time.monotonic()
        else: 
            del _uuid_cache[username]
            raise RuntimeError(f"Could not get UUID <{response.status_code}> [{response.content}]")
        if len(_uuid_cache) > UUID_CACHE_LIMIT:
            _drop_uuid_cache()
    return _uuid_cache[username]["uuid"]


_profiles_cache = {}
PROFILES_CACHE_LIMIT = 32
def _drop_profiles_cache() -> None:
    oldest = min(_profiles_cache, key=lambda x: _profiles_cache[x]["timestamp"])
    del _profiles_cache[oldest]

def get_profiles(uuid: str, data_lifetime: int = 600) -> list:
    if uuid not in _profiles_cache:
        _profiles_cache[uuid] = {
            "timestamp": float("-inf"),
            "data": {},
        }
    if time.monotonic()-_profiles_cache[uuid]["timestamp"] >= data_lifetime:
        response = requests.get("https://api.hypixel.net/v2/skyblock/profiles", headers=HEADERS, params={"uuid": uuid}, timeout=10)
        if response.status_code == 200:
            _profiles_cache[uuid]["data"] = response.json()["profiles"] or []
            _profiles_cache[uuid]["timestamp"] = time.monotonic()
        else: 
            del _profiles_cache[uuid]
            raise RuntimeError(f"Could not get profile data <{response.status_code}> [{response.content}]")
        if len(_profiles_cache) > PROFILES_CACHE_LIMIT:
            _drop_profiles_cache()
    return _profiles_cache[uuid]["data"]


def get_profile_id(profile_name: str, uuid: str, profiles: list | None = None) -> str:
    if profiles is None:
        profiles = get_profiles(uuid)
    for profile in profiles:
        if profile["cute_name"].lower() == profile_name.lower():
            return profile["profile_id"]
    raise KeyError(f"Could not find profile {profile_name} in user profiles")


_garden_cache = {}
GARDEN_CACHE_LIMIT = 256
def _garden_cache_drop() -> None:
    oldest = min(_garden_cache, key=lambda x: _garden_cache[x]["timestamp"])
    del _garden_cache[oldest]
    
def get_garden_data(profile_id: str, data_lifetime: int = 600) -> dict:
    if profile_id not in _garden_cache:
        _garden_cache[profile_id] = {
            "timestamp": float("-inf"),
            "data": {},
        }
    if time.monotonic() - _garden_cache[profile_id]["timestamp"] >= data_lifetime:
        response = requests.get("https://api.hypixel.net/v2/skyblock/garden", headers=HEADERS, params={"profile": profile_id}, timeout=10)
        if response.status_code == 200:
            _garden_cache[profile_id]["timestamp"] = time.monotonic()
            _garden_cache[profile_id]["data"] = response.json()["garden"]
        else:
            del _garden_cache[profile_id]
            raise RuntimeError(f"Could not get garden data <{response.status_code}> [{response.content}]")
        if len(_garden_cache) > GARDEN_CACHE_LIMIT:
            _garden_cache_drop()
    return _garden_cache[profile_id]["data"]


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
_bz_lock = threading.Lock()
def get_bz_data(data_lifetime: int = 300) -> dict:
    with _bz_lock:
        if time.monotonic() - _bz_cache["timestamp"] >= data_lifetime:
            response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar", headers=HEADERS, timeout=10)
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