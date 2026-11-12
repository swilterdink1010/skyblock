## Overview

Composter Tools is an app that fetches Bazaar, Profile data, and Garden data from the API to calculate optimal composter upgrades for a given profile.

## Caching

The API is called by a single module that is shared across all web instances independent of each web session's cache. The module makes requests to the API and caches the result, no matter if it is a success or a failure.

1. If the web instance requests an item from the API module, the module will check if the data is stored in the cache. 
2. If it is in the cache, the module checks whether the data is within its data lifetime (different per request type). 
3. If it is within the data lifetime, the module returns the cached value without making an API call. 

    If it is not within the data lifetime, the module makes a request to the API and caches the new value.

## Requests

### Skyblock Profiles requests
- A successful response is stored in a cache with a size limit of 32 users.
- An unsuccessful response is stored in a cache with a size limit of 4096 users.
> The profile caches have a data lifetime of 600 seconds, or 10 minutes.

### Skyblock Garden requests
- A successful response is stored in a cache with a size limit of 256 profiles.
- An unsuccessful response is stored in a cache with a size limit of 4096 profiles.
> The garden caches have a data lifetime of 600 seconds, or 10 minutes.

### Skyblock Bazaar requests
- A successful response is stored in a cache that stores one set of bazaar data.
- An unsuccessful response is not stored in a cache.
> The bazaar cache has a data lifetime of 300 seconds, or 5 minutes.

## API Usage

For each unique user of the tool, I expect one profile request every 10 minutes and one garden request every 10 minutes.

I expect a constant one bazaar request every 5 minutes that the tool is in use. If the tool is not in use, it does not make any requests.