import time
from math import ceil, floor

import forecast
from helpers import add_ints_avg, get_timestamp


def forecast_price(self) -> dict:
    """Returns the price forecast"""
    return forecast.price(self)


def forecast_climate(self) -> dict:
    """Returns the climate forecast"""
    return forecast.climate(self)


def current_price(self, type: str = "total") -> None:
    """
    Returns the current kwh price (by default the total price)

    `type` accepts `total` (default), `raw_price`, or `tax`
    """

    if type not in ["total", "raw_price", "tax"]:
        raise ValueError("Type is not one of `total`, `raw_price`, or `tax`")

    prices = forecast.price(self)
    return prices[int(time.strftime("%H"))][f"kwh_{type}"]


def current_green_energy(self) -> None:
    """Returns the current green energy percent"""

    climates = forecast.climate(self)
    return climates[int(time.strftime("%H"))]["green_energy_percent"]


def current_co2_intensity(self) -> None:
    """Returns the current co2 intensity"""

    climates = forecast.climate(self)
    return climates[int(time.strftime("%H"))]["co2_intensity"]


def price_at(self, timestamp: str) -> dict:
    """
    Returns the price at `timestamp`

    `timestamp` is in the format "2022-03-19T08:00:00"
    """
    prices = forecast.price(self)

    timestamp = get_timestamp(timestamp)

    for v in prices.values():
        if v["start_time"] == timestamp:
            return v

    return {}


def climate_at(self, timestamp: str | int) -> dict:
    """
    Returns the climate at `timestamp`

    `timestamp` is in the format "2022-03-19T08:00:00" or
    an hour `8` or `36`

    """
    climates = forecast.climate(self)

    timestamp = get_timestamp(timestamp)

    for v in climates.values():
        if v["start_time"] == timestamp:
            return v

    return {}


# for *_interval we should consider apartments
# that can't wash during the night
def best_interval(self, interval: int = 1, items: int = 3) -> dict:
    """
    Returns the greenest/cheapest interval(s) depending
    on primary motivation, but in case of `both` will always
    have a slight green bias
    """
    if self.motivation == "economy":
        return cheapest_interval(self, interval, items)
    elif self.motivation == "both":
        cheapest = cheapest_interval(self, interval, items)
        greenest = greenest_interval(self, interval, items)

        uniq = list()
        for i in cheapest + greenest:
            if i not in uniq:
                uniq.append(i)

        # We can still have a green bias ;-)
        n_green = ceil(items / 2)
        n_cheap = floor(items / 2)

        return sorted(
            uniq[0:n_green] + uniq[n_green : n_green + n_cheap],
            key=lambda x: (
                x["interval_avg_green_energy_percent_estimate"],  # prefer non-estimates
                x["interval_avg_kwh_price_estimate"],
                -x["interval_avg_green_energy_percent"],
                x["interval_avg_kwh_price"],
            ),
        )
    else:
        return greenest_interval(self, interval, items)


def cheapest_interval(self, interval: int = 1, items: int = 3) -> list:
    """
    Returns the n (`items`) cheapest start_time
    for the given `interval` (in hours)
    """
    prices = forecast.price(self)

    cheap_keys = list()

    for key in prices.keys():
        interval_price = 0
        interval_energy = list()

        try:
            for i in range(interval):
                interval_price += prices[key + i]["kwh_total"]
                interval_energy.append(
                    climate_at(self, prices[key + i]["start_time"]).get(
                        "green_energy_percent", "N/A"
                    )
                )
        except KeyError:
            break

        energy, estimate = add_ints_avg(interval_energy)

        cheap_keys.append(
            {
                "start_time": prices[key]["start_time"],
                "interval_hours": interval,
                "interval_avg_kwh_price": round(interval_price / interval, 2),
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": energy,
                "interval_avg_green_energy_percent_estimate": estimate,
            }
        )

    return sorted(
        cheap_keys,
        key=lambda x: (
            x["interval_avg_kwh_price"],
            x["interval_avg_green_energy_percent_estimate"],  # prefer non-estimates
            -x["interval_avg_green_energy_percent"],
        ),
    )[0:items]


def greenest_interval(self, interval: int = 1, items: int = 3) -> list:
    """
    Returns the n (`items`) greenest start_time
    for a given `interval` (in hours)
    """
    climates = forecast.climate(self)

    green_keys = list()

    for key in climates.keys():
        interval_energy = 0
        interval_price = list()

        try:
            for i in range(interval):
                interval_energy += climates[key + i]["green_energy_percent"]
                interval_price.append(
                    price_at(self, climates[key + i]["start_time"]).get(
                        "kwh_total", "N/A"
                    )
                )
        except KeyError:
            break

        price, estimate = add_ints_avg(interval_price)

        green_keys.append(
            {
                "start_time": climates[key]["start_time"],
                "interval_hours": interval,
                "interval_avg_kwh_price": price,
                "interval_avg_kwh_price_estimate": estimate,
                "interval_avg_green_energy_percent": round(
                    interval_energy / interval, 2
                ),
                "interval_avg_green_energy_percent_estimate": False,
            }
        )

    return sorted(
        green_keys,
        key=lambda x: (
            -x["interval_avg_green_energy_percent"],
            x["interval_avg_kwh_price_estimate"],  # prefer non-estimates
            x["interval_avg_kwh_price"],
        ),
    )[0:items]
