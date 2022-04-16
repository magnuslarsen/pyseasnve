import datetime

import requests

from .constants import COPI_API, KEY_TIMESTAMP_FMT
from .helpers import headers, utc_to_dk


def pretty_label(t: datetime.datetime, resolution: str) -> str:
    """Return a pretty label for `t` using the specified resolution

    :param t: a timestamp used to format the label
    :type t: datetime.datetime
    :param resolution: used to determine the format of the label
    :type resolution: str
    :rtype: str
    """
    if resolution not in ["hourly", "daily", "weekly", "monthly", "yearly"]:
        raise ValueError("resolution is not one of 'hourly', 'daily', 'weekly', 'monthly', 'yearly'")

    r = ""
    if resolution == "hourly":
        r = t.hour
    elif resolution == "daily":
        r = t.strftime("%A")
    elif resolution == "weekly":
        r = t.strftime("%W")
    elif resolution == "monthly":
        r = t.strftime("%B")
    elif resolution == "yearly":
        r = t.year

    return str(r)


def consumption(self, resolution: str = "weekly") -> list:
    """Return previous consumption stats, using desired resoution

    :param self: self
    :param resolution: one of 'hourly', 'daily', 'weekly', 'monthly', 'yearly'
    :type resolution: str
    :rtype: list
    """
    if resolution not in ["hourly", "daily", "weekly", "monthly", "yearly"]:
        raise ValueError("resolution is not one of 'hourly', 'daily', 'weekly', 'monthly', 'yearly'")

    if self._cache.is_cached(f"consumption_{resolution}"):
        return self._cache.get(f"consumption_{resolution}")

    r = requests.get(f"{COPI_API}/consumptionPage/{self._external_id}/{resolution}", headers=headers(self))
    r.raise_for_status()

    data = list()
    json = r.json()["data"][0]["consumptions"]

    for period in json:
        s = utc_to_dk(period["start"])
        e = utc_to_dk(period["end"])

        data.append(
            {
                "start_time": s.strftime(KEY_TIMESTAMP_FMT),
                "end_time": e.strftime(KEY_TIMESTAMP_FMT),
                "used_kwh": period["kWh"],
                "label": pretty_label(s, resolution),
            }
        )

    self._cache.set(f"consumption_{resolution}", data)

    return data
