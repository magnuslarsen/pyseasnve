import datetime


class cache:
    """A class to cache data for PySeasNVE."""

    def __init__(self, expiry_hour: int = 0):
        self.expiry_hour = expiry_hour
        self.collection = {}

    def get(self, key: str) -> dict:
        """Get the cached data.

        :param self: self
        :param key: the key of the cache data
        :type key: str
        :rtype: dict
        """
        if self.is_cached(key):
            return self.collection[key]["data"]
        else:
            return {}

    def set(self, key: str, data: dict) -> None:
        """Set the cache data.

        :param self: self
        :param key: the key of the cache data
        :type key: str
        :param data: the data to cache
        :type data: dict
        :rtype: None
        """
        self.collection[key] = {"cached_hour": datetime.datetime.now().hour, "data": data}

    def keys(self) -> list:
        """Return all keys in cache.

        :param self: self
        :rtype: list
        """
        return list(self.collection.keys())

    def is_cached(self, key: str):
        """Check if `key` is cached.

        :param key: the key of the cache data
        :type key: str
        :rtype: bool
        """

        if key in self.collection:
            hour = datetime.datetime.now().hour
            if hour == self.expiry_hour and self.collection[key]["cached_hour"] != self.expiry_hour:
                return False
            else:
                return True
        else:
            return False
