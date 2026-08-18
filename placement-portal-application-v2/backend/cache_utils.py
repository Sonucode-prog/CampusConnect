from cache import cache


def get_cache_version(name):
    key = f"cache_version:{name}"

    version = cache.get(key)

    if version is None:
        version = 1
        cache.set(key, version, timeout=0)

    return version


def refresh_cache(name):
    key = f"cache_version:{name}"

    version = get_cache_version(name)

    cache.set(key, version + 1, timeout=0)