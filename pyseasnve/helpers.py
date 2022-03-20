import time

import constants as c
import requests
from exceptions import LoginError


def login(self, password) -> None:
    """Attempts to login to the API"""

    self._public_ip = public_ip()

    body = {"customer": self.username, "password": password}

    try:
        r = requests.post(
            f"{c.PRICE_API}/authenticate",
            data=body,
            headers=headers(self),
        )
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise LoginError(f"Failed to login: {e}")

    json = r.json()

    self._token = json["token"]
    self._zip_code = json["address"]["zip_code"]


def init_vars(self) -> None:
    """Sets all the variables required for all other functions"""

    r = requests.get(f"{c.COPI_API}/profile", headers=headers(self))
    r.raise_for_status()

    json = r.json()

    self.motivation = json["primaryMotivation"]
    self.accommodation_type = json["accommodationType"]

    # grid_area is only mentioned in forward-prices...
    r = requests.get(
        f"{c.PRICE_API}/forward-prices/{self._zip_code}",
        headers=headers(self),
    )
    r.raise_for_status()

    json = r.json()
    self._grid_area = json["0"]["grid_area"]


def headers(self) -> dict:
    """Sets appropiate headers for API calls"""
    return {
        "X-Customer-Ip": self._public_ip,
        "Authorization": self._token,
    }


def public_ip() -> str:
    """Returns the public ip"""
    return requests.get("https://api.ipify.org").text


def add_ints_avg(raw_list: list) -> list:
    """
    Returns the average of non-`int`s in `raw_list`. If any `str` is found,
    add the average for each. Incase only `str` return 0

    Returns a list in the format `(added_nums_avg: float, estimation: bool)`
    """
    estimate = False
    num = 0
    str_count = [type(n) for n in raw_list].count(str)

    if str_count > 0:
        estimate = True
        non_str_count = len(raw_list) - str_count

        # Add the average for each "N/A" in the list. Incase we
        # only have strings, just add 0. We have no idea
        if non_str_count > 0:
            num = sum(n for n in raw_list if type(n) != str)
            num += (num / non_str_count) * str_count

            num = num / len(raw_list)
        else:
            num = 0.0

    else:
        num = sum(raw_list) / len(raw_list)

    return (round(num, 2), estimate)


def get_timestamp(timestamp: int | str) -> str:
    """
    Returns a timestamp for the given hour of `timestamp`,
    or simply returns `timestamp` if already formatted correctly
    """
    if type(timestamp) == int or (type(timestamp) == str and timestamp.isnumeric()):
        timestamp = int(timestamp)

        if timestamp > 24:
            day = int(time.strftime("%d")) + 1
            hour = timestamp - 24

            return time.strftime(
                f"%Y-%m-{str(day).zfill(2)}T{str(hour).zfill(2)}:00:00"
            )
        else:
            return time.strftime(f"%Y-%m-%dT{str(timestamp).zfill(2)}:00:00")

    return timestamp
