import requests, os, time, threading
from typing import Literal
from dotenv import load_dotenv
from enum import Enum


class BadAPICallCode(Enum):
    NO_UUID = 405
    NO_PROFILE_DATA = 406
    NO_GARDEN_DATA = 407
    NO_BZ_DATA = 408
    BAD_API_KEY = 409


class BadAPICallError(Exception):
    def __init__(self, message: str, code: BadAPICallCode | int = 400):
        super().__init__(message)
        self.code = code


load_dotenv()
HYPIXEL_API_KEY = os.getenv("HYPIXEL_API_KEY")
if not HYPIXEL_API_KEY:
    raise RuntimeError("HYPIXEL_API_KEY is not set")
HEADERS = {
    "API-Key": HYPIXEL_API_KEY,
}


def is_valid_username(username: str) -> bool:
    if len(username) < 3 or len(username) > 16:
        return False
    for char in username:
        if char.lower() not in "1234567890abcdefghijklmnopqrstuvwxyz_":
            return False
    return True


_uuid_cache = {}
UUID_CACHE_LIMIT = 4096
def _drop_uuid_cache() -> None:
    oldest = min(_uuid_cache, key=lambda x: _uuid_cache[x]["timestamp"])
    del _uuid_cache[oldest]
    
_bad_uuid_cache = {}
BAD_UUID_CACHE_LIMIT = 4096
def _drop_bad_uuid_cache() -> None:
    oldest = min(_bad_uuid_cache, key=lambda x: _bad_uuid_cache[x])
    del _bad_uuid_cache[oldest]
    
def get_uuid(username: str, data_lifetime: int = 86400) -> str:
    if not is_valid_username(username):
        raise ValueError(f"Invalid {username = }")
    username = username.lower()
    if username in _bad_uuid_cache:
        if time.monotonic()-_bad_uuid_cache[username] >= data_lifetime:
            del _bad_uuid_cache[username]
        else: raise BadAPICallError(f"Could not get UUID for {username = }", BadAPICallCode.NO_UUID)
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
            _bad_uuid_cache[username] = time.monotonic()
            if len(_bad_uuid_cache) > BAD_UUID_CACHE_LIMIT:
                _drop_bad_uuid_cache()
            raise BadAPICallError(f"Could not get UUID for {username = }", BadAPICallCode.NO_UUID)
        if len(_uuid_cache) > UUID_CACHE_LIMIT:
            _drop_uuid_cache()
    return _uuid_cache[username]["uuid"]


_profiles_cache = {}
PROFILES_CACHE_LIMIT = 32
def _drop_profiles_cache() -> None:
    oldest = min(_profiles_cache, key=lambda x: _profiles_cache[x]["timestamp"])
    del _profiles_cache[oldest]

_bad_profiles_cache = {}
BAD_PROFILES_CACHE_LIMIT = 4096
def _drop_bad_profiles_cache() -> None:
    oldest = min(_profiles_cache, key=lambda x: _bad_profiles_cache[x])
    del _bad_profiles_cache[oldest]

def get_profiles(uuid: str, data_lifetime: int = 600) -> list:
    if uuid in _bad_profiles_cache:
        if time.monotonic()-_bad_profiles_cache[uuid] >= data_lifetime:
            del _bad_profiles_cache[uuid]
        else: raise BadAPICallError(f"Could not get profile data for {uuid = }", BadAPICallCode.NO_PROFILE_DATA)
    if uuid not in _profiles_cache:
        _profiles_cache[uuid] = {
            "timestamp": float("-inf"),
            "data": {},
        }
    if time.monotonic()-_profiles_cache[uuid]["timestamp"] >= data_lifetime:
        response = requests.get("https://api.hypixel.net/v2/skyblock/profiles", headers=HEADERS, params={"uuid": uuid}, timeout=10)
        match response.status_code:
            case 200:
                _profiles_cache[uuid]["data"] = response.json()["profiles"] or []
                _profiles_cache[uuid]["timestamp"] = time.monotonic()
            case 403:
                del _profiles_cache[uuid]
                raise BadAPICallError("Bad API key", BadAPICallCode.BAD_API_KEY)
            case _:
                del _profiles_cache[uuid]
                _bad_profiles_cache[uuid] = time.monotonic()
                if len(_bad_profiles_cache) > PROFILES_CACHE_LIMIT:
                    _drop_bad_profiles_cache()
                raise BadAPICallError(f"Could not get profile data for {uuid = }", BadAPICallCode.NO_PROFILE_DATA)
        if len(_profiles_cache) > PROFILES_CACHE_LIMIT:
            _drop_profiles_cache()
    return _profiles_cache[uuid]["data"]


def get_profile_id(profile_name: str, uuid: str, profiles: list | None = None) -> str:
    if profiles is None:
        profiles = get_profiles(uuid)
    for profile in profiles:
        if profile["cute_name"].lower() == profile_name.lower():
            return profile["profile_id"]
    raise KeyError(f"Could not find {profile_name = } in user profiles")


_garden_cache = {}
GARDEN_CACHE_LIMIT = 256
def _garden_cache_drop() -> None:
    oldest = min(_garden_cache, key=lambda x: _garden_cache[x]["timestamp"])
    del _garden_cache[oldest]
    
_bad_garden_cache = {}
BAD_GARDEN_CACHE_LIMIT = 4096
def _drop_bad_garden_cache() -> None:
    oldest = min(_bad_garden_cache, key=lambda x: _bad_garden_cache[x])
    del _bad_garden_cache[oldest]
    
def get_garden_data(profile_id: str, data_lifetime: int = 600) -> dict:
    if profile_id in _bad_garden_cache:
        if time.monotonic()-_bad_garden_cache[profile_id] >= data_lifetime:
            del _bad_garden_cache[profile_id]
        else: raise BadAPICallError(f"Could not get garden data for {profile_id = }", BadAPICallCode.NO_GARDEN_DATA)
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
            _bad_garden_cache[profile_id] = time.monotonic()
            if len(_bad_garden_cache) > BAD_GARDEN_CACHE_LIMIT:
                _drop_bad_garden_cache()
            raise BadAPICallError(f"Could not get garden data for {profile_id = }", BadAPICallCode.NO_GARDEN_DATA)
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
        if time.monotonic()-_bz_cache["timestamp"] >= data_lifetime:
            response = requests.get("https://api.hypixel.net/v2/skyblock/bazaar", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                _bz_cache["timestamp"] = time.monotonic()
                _bz_cache["data"] = response.json()["products"]
            else: raise BadAPICallError(f"Could not get bazaar data", BadAPICallCode.NO_BZ_DATA)
    return _bz_cache["data"]


def get_bz_price(id: str, field: Literal["buyPrice", "sellPrice"] = "buyPrice") -> float:
    if not get_bz_data().get(id):
        raise KeyError(f"Invalid item {id = }")
    return get_bz_data()[id]["quick_status"][field]


def main() -> None:
    pass
    
    
if __name__ == "__main__":
    main()