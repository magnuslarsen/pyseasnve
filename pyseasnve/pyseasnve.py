"""Main module."""


class LoginError(Exception):
    pass


class PySeasNVE:
    from .core import (best_interval, cheapest_interval, climate_at,
                       current_co2_intensity, current_green_energy,
                       current_price, forecast_climate, forecast_price,
                       greenest_interval, price_at)

    def __init__(self, username, password):
        from .helpers import init_vars, login

        self.username = username

        # Private vars
        self._token = ""
        self._grid_area = ""
        self._zip_code = ""
        self._public_ip = ""
        self._cached_forecast_price = {}
        self._cached_forecast_climate = {}

        # Properties
        self._accommodation_type = ""
        self._motivation = ""

        # Login instantly, skipping saving the plain text password in self
        login(self, password)

        # Preload variables
        init_vars(self)

    @property
    def motivation(self):
        return self._motivation

    @motivation.setter
    def motivation(self, m):
        if m in ["economy", "environment", "both"]:
            self._motivation = m
        else:
            raise ValueError("motivation can only be one of `economy`, `environment`, or `both`")

    @property
    def accommodation_type(self):
        return self._accommodation_type

    @accommodation_type.setter
    def accommodation_type(self, t):
        if t in ["apartment", "house"]:
            self._accommodation_type = t
        else:
            raise ValueError("accommodation_type can only be `apartment` or `house`")
