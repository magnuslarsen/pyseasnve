import datetime
import time

import requests

from .constants import CLIMATE_API, KEY_TIMESTAMP_FMT, PRICE_API
from .helpers import headers, is_cached, utc_to_dk


def price(self) -> dict:
    """Get the price forecast."""
    if is_cached(self._cached_forecast_price):
        return self._cached_forecast_price["data"]

    r = requests.get(
        f"{PRICE_API}/forward-prices/{self._zip_code}",
        headers=headers(self),
    )
    json = r.json()

    # dict.$HOUR is electric prices without tariffs
    # dict.distribution_prices are tariffs, but only for today (?)
    prices = {}
    tariff_prices = json["distribution_prices"][0]["prices"]

    for i in range(48):
        # Sometimes they don't bring all 48 hours
        # Break out early in such case
        try:
            o = json[str(i)]
        except KeyError:
            break

        t = datetime.datetime.strptime(o["valid_from"], "%Y-%m-%d %H:%M:%S")

        mday = int(time.strftime("%d"))
        hour = int(time.strftime("%H"))
        if t.day < mday or (t.day == mday and t.hour < hour):
            # A forecast doesn't account for past time
            continue

        if i >= 24:
            # The tariff price only has hours for today (?); it looks like
            # they are reusing the prices again for tomorrow
            kwh_tariffs = round(tariff_prices[i - 24]["price"]) / 100
        else:
            kwh_tariffs = round(tariff_prices[i]["price"]) / 100

        kwh_raw_price = round(o["price"]) / 100
        kwh_total = round(kwh_raw_price + kwh_tariffs, 2)

        # The API only updates prices every other day it seems.
        # Correct in case we start at 2nd day of prices
        if i >= 24 and i - 24 not in prices.keys():
            key = i - 24
        else:
            key = i

        prices[key] = {
            "start_time": t.strftime(KEY_TIMESTAMP_FMT),
            "kwh_raw_price": kwh_raw_price,
            "kwh_tariffs": kwh_tariffs,
            "kwh_total": kwh_total,
        }

    # "cache" the result, as it only changes every hour 00:00
    self._cached_forecast_price = {
        "cached_hour": datetime.datetime.now().hour,
        "data": prices,
    }

    return prices


def climate(self) -> dict:
    """Get the climate forecast."""
    if is_cached(self._cached_forecast_climate):
        return self._cached_forecast_climate["data"]

    r = requests.get(
        f"{CLIMATE_API}/energydata/DK-{self._grid_area}",
        headers=headers(self),
    )
    json = r.json()

    sorted_climate = sorted(json, key=lambda x: x["start"])
    climates = {}

    for i in sorted_climate:
        # For climates, they output dates in UTC
        t = utc_to_dk(i["start"])
        offset = t.utcoffset().seconds

        mday = int(time.strftime("%d"))
        hour = int(time.strftime("%H")) - offset / 3600  # also correct time.now()
        if t.day < mday or (t.day == mday and t.hour < hour):
            # A forecast doesn't account for past time
            continue

        c_biomass = i["powerConsumptionBreakdown"]["biomass"] or 0
        c_coal = i["powerConsumptionBreakdown"]["coal"] or 0
        c_gas = i["powerConsumptionBreakdown"]["gas"] or 0
        c_geothermal = i["powerConsumptionBreakdown"]["geothermal"] or 0
        c_hydro = i["powerConsumptionBreakdown"]["hydro"] or 0
        c_nuclear = i["powerConsumptionBreakdown"]["nuclear"] or 0
        c_oil = i["powerConsumptionBreakdown"]["oil"] or 0
        c_solar = i["powerConsumptionBreakdown"]["solar"] or 0
        c_wind = i["powerConsumptionBreakdown"]["wind"] or 0
        c_unknown = i["powerConsumptionBreakdown"]["unknown"] or 0

        # This seems to be what they qualify as green/black energy
        c_green = c_biomass + c_geothermal + c_hydro + c_nuclear + c_solar + c_wind
        c_total = c_green + c_coal + c_gas + c_oil + c_unknown

        c_green_energy_percent = round(c_green / c_total * 100, 2)

        if t.day > int(time.strftime("%d")):
            key = t.hour + 24
        else:
            key = t.hour

        climates[key] = {
            "start_time": t.strftime(KEY_TIMESTAMP_FMT),
            "green_energy_percent": c_green_energy_percent,
            "co2_intensity": i["co2_intensity"],
            "consumption_breakdown_percent": {
                "biomass": round(c_biomass / c_total * 100, 2),
                "coal": round(c_coal / c_total * 100, 2),
                "gas": round(c_gas / c_total * 100, 2),
                "geothermal": round(c_geothermal / c_total * 100, 2),
                "hydro": round(c_hydro / c_total * 100, 2),
                "nuclear": round(c_nuclear / c_total * 100, 2),
                "oil": round(c_oil / c_total * 100, 2),
                "solar": round(c_solar / c_total * 100, 2),
                "wind": round(c_wind / c_total * 100, 2),
                "unknown": round(c_unknown / c_total * 100, 2),
            },
        }

    # "cache" the result, as it only changes every hour 00:00
    self._cached_forecast_climate = {
        "cached_hour": datetime.datetime.now().hour,
        "data": climates,
    }

    return climates
