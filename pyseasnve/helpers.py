import time

import constants as c
import requests
from exceptions import LoginError


def login(self, password) -> None:
    """Attempt to login to the API."""
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
    """Set all the variables required for all other functions."""
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
    """Set appropiate headers for API calls."""
    return {
        "X-Customer-Ip": self._public_ip,
        "Authorization": self._token,
    }


def public_ip() -> str:
    """Return the public ip."""
    return requests.get("https://api.ipify.org").text


def add_ints_avg(raw_list: list) -> set:
    """Return the average of `raw_list`, trying to estimate if necessary.

    :param raw_list: a list of numbers and `N/A`s
    :type raw_list: list
    :rtype: set
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


def get_timestamp(t: int | str) -> str:
    """
    Return `t` or the timestamp at hour `t` if only an hour was provided.

    :param t: a timestamp or an hour
    :type t: int | str
    :rtype: str
    """
    if type(t) == int or (type(t) == str and t.isnumeric()):
        t = int(t)

        if t > 24:
            day = int(time.strftime("%d")) + 1
            hour = t - 24

            return time.strftime(f"%Y-%m-{str(day).zfill(2)}T{str(hour).zfill(2)}:00:00")
        else:
            return time.strftime(f"%Y-%m-%dT{str(t).zfill(2)}:00:00")

    return t
