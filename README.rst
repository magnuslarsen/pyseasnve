=========
PySeasNVE
=========


.. image:: https://img.shields.io/pypi/v/pyseasnve.svg
        :target: https://pypi.org/project/pyseasnve/

.. image:: https://readthedocs.org/projects/pyseasnve/badge/?version=latest
        :target: https://pyseasnve.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




An unofficial class to interact (read-only) with the Seas-NVE API

You'll need to own an account over at https://seas-nve.dk/


* Free software: GNU General Public License v3
* Documentation: https://pyseasnve.readthedocs.io.


Features
--------

* Current pricing & climate stats
* Forecasts for pricing and climate stats
* The next cheapest/greenest/mixed period (for any given intervals)

TODO:

* Billing stats?
* Long-term stats (i.e. weekly/monthly/yearly usage) (50% done)
* Possibility to set configuration values via the API


Usage
------------
.. code-block:: python

        # Install
        python3 -m pip install -U pyseasnve

        # Login
        >>> from pyseasnve import PySeasNVE
        >>> seas = PySeasNVE('test@email.com', 'secretPassword')

        # Current price + climate stats
        >>> seas.current_price()
        1.68 # DKK/kWh
        >>> seas.current_green_energy()
        75.68 # %
        >>> seas.current_co2_intensity()
        188 # gCO2eq/kWh

        # Get the price & climate at some hour
        >>> seas.price_at(9)
        {'start_time': '2022-03-26T09:00:00', 'kwh_raw_price': 1.48, 'kwh_tariffs': 1.56, 'kwh_total': 3.04}
        >>> seas.price_at("2022-03-26T18:00:00")
        {'start_time': '2022-03-26T18:00:00', 'kwh_raw_price': 2.44, 'kwh_tariffs': 2.05, 'kwh_total': 4.49}

        >>> seas.climate_at(26)
        {'start_time': '2022-03-27T02:00:00', 'green_energy_percent': 68.7, 'co2_intensity': 251, 'consumption_breakdown_percent': {'biomass': 23.94, 'coal': 21.6, 'gas': 8.36, 'geothermal': 0.0, 'hydro': 1.7, 'nuclear': 7.22, 'oil': 0.0, 'solar': 2.83, 'wind': 33.0, 'unknown': 1.35}}

        # Next two cheapest 4-hour intervals
        >>> seas.cheapest_interval(4, 2)
        [{'start_time': '2022-03-20T12:00:00', 'interval_hours': 4, 'interval_avg_kwh_price': 1.59, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}, {'start_time': '2022-03-20T11:00:00', 'interval_hours': 4, 'interval_avg_kwh_price': 1.6, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}]

        # Next greenest 1-hour interval
        >>> seas.greenest_interval(1, 1)
        [{'start_time': '2022-03-20T12:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}]

        # Or simply use the "best" method, depending on your motivation in SEAS-NVE
        >>> seas.best_interval()
        [{'start_time': '2022-03-20T12:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}, {'start_time': '2022-03-20T13:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}, {'start_time': '2022-03-20T14:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}]

You can access the forecasts directly aswell, to write you own wrapper code around it.
If you find something is missing, please raise an issue or submit the code :-)


.. code-block:: python

        >>> seas.forecast_price()
        # output not shown
        >>> seas.forecast_climate()
        # output not shown


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
