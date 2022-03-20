=========
PySeasNVE
=========


.. image:: https://img.shields.io/pypi/v/pyseasnve.svg
        :target: https://pypi.python.org/pypi/pyseasnve

.. image:: https://img.shields.io/travis/magnuslarsen/pyseasnve.svg
        :target: https://travis-ci.com/magnuslarsen/pyseasnve

.. image:: https://readthedocs.org/projects/pyseasnve/badge/?version=latest
        :target: https://pyseasnve.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




An unofficial class to interact (read only) with the Seas-NVE API

You'll need to own an account over at https://seas-nve.dk/


* Free software: GNU General Public License v3
* Documentation: https://pyseasnve.readthedocs.io.


Features
--------

* Current pricing & climate stats
* Forecasts for pricing and climate stats
* The next cheapest/greenest period (for any given intervals)

TODO:

* Billing stats?
* Long-term stats (i.e. weekly/monthly/yearly usage)
* Possibility to set configuration values via the API


Introduction
------------
.. code-block:: python

        # Login
        >>> from pyseasnve import PySeasNVE
        >>> seas = PySeasNVE('test@email.com', 'secretPassword')

        # Current price + climate stats
        >>> seas.current_price()
        1.68 # DKK/kwh
        >>> seas.current_green_energy()
        75.68 # %
        >>> seas.current_co2_intensity()
        188 # unknown unit

        # Next two cheapest 4-hour intervals
        >>> seas.cheapest_interval(4, 2)
        [{'start_time': '2022-03-20T12:00:00', 'interval_hours': 4, 'interval_avg_kwh_price': 1.59, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}, {'start_time': '2022-03-20T11:00:00', 'interval_hours': 4, 'interval_avg_kwh_price': 1.6, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}]

        # Next greenest 1-hour interval
        >>> seas.greenest_interval(1, 1)
        [{'start_time': '2022-03-20T12:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}]

        # Or simply use the "best" method, depending on your motivation in SEAS-NVE
        >>> seas.best_interval()
        [{'start_time': '2022-03-20T12:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}, {'start_time': '2022-03-20T13:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}, {'start_time': '2022-03-20T14:00:00', 'interval_hours': 1, 'interval_avg_kwh_price': 1.57, 'interval_avg_kwh_price_estimate': False, 'interval_avg_green_energy_percent': 75.68, 'interval_avg_green_energy_percent_estimate': False}]

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
