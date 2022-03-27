#!/usr/bin/env python

"""Tests for `pyseasnve` package."""


import unittest

from pyseasnve import DummyPySeasNVE


class TestPyseasnve(unittest.TestCase):
    """Tests for `pyseasnve` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.seas = DummyPySeasNVE("test", "test")
        self.seas._cached_forecast_price = {
            "cached_hour": 13,
            "data": {
                13: {
                    "start_time": "2022-03-20T13:00:00",
                    "kwh_raw_price": 0.01,
                    "kwh_tariffs": 1.56,
                    "kwh_total": 1.57,
                },
                14: {
                    "start_time": "2022-03-20T14:00:00",
                    "kwh_raw_price": 0.18,
                    "kwh_tariffs": 1.59,
                    "kwh_total": 1.77,
                },
                15: {
                    "start_time": "2022-03-20T15:00:00",
                    "kwh_raw_price": 0.18,
                    "kwh_tariffs": 2.01,
                    "kwh_total": 2.19,
                },
            },
        }
        self.seas._cached_forecast_climate = {
            "cached_hour": 13,
            "data": {
                13: {
                    "start_time": "2022-03-20T13:00:00",
                    "green_energy_percent": 85.68,
                    "co2_intensity": 204,
                    "consumption_breakdown_percent": {
                        "biomass": 18.64,
                        "coal": 16.9,
                        "gas": 5.41,
                        "geothermal": 0.0,
                        "hydro": 13.09,
                        "nuclear": 10.02,
                        "oil": 0.0,
                        "solar": 3.94,
                        "wind": 29.99,
                        "unknown": 2.0,
                    },
                },
                14: {
                    "start_time": "2022-03-20T14:00:00",
                    "green_energy_percent": 75.68,
                    "co2_intensity": 182,
                    "consumption_breakdown_percent": {
                        "biomass": 18.64,
                        "coal": 16.9,
                        "gas": 5.41,
                        "geothermal": 0.0,
                        "hydro": 13.09,
                        "nuclear": 10.02,
                        "oil": 0.0,
                        "solar": 3.94,
                        "wind": 29.99,
                        "unknown": 2.0,
                    },
                },
                15: {
                    "start_time": "2022-03-20T15:00:00",
                    "green_energy_percent": 80.68,
                    "co2_intensity": 194,
                    "consumption_breakdown_percent": {
                        "biomass": 18.64,
                        "coal": 16.9,
                        "gas": 5.41,
                        "geothermal": 0.0,
                        "hydro": 13.09,
                        "nuclear": 10.02,
                        "oil": 0.0,
                        "solar": 3.94,
                        "wind": 29.99,
                        "unknown": 2.0,
                    },
                },
            },
        }

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.seas

    def test_greenest_1_interval(self):
        """Test the greenest_interval with interval=1"""
        expected_result = [
            {
                "start_time": "2022-03-20T13:00:00",
                "interval_hours": 1,
                "interval_avg_kwh_price": 1.57,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 85.68,
                "interval_avg_green_energy_percent_estimate": False,
            },
            {
                "start_time": "2022-03-20T15:00:00",
                "interval_hours": 1,
                "interval_avg_kwh_price": 2.19,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 80.68,
                "interval_avg_green_energy_percent_estimate": False,
            },
        ]
        actual_result = self.seas.greenest_interval(1, 2)

        self.assertListEqual(actual_result, expected_result)

    def test_greenest_2_interval(self):
        """Test the greenest_interval function with interval=2"""
        expected_result = [
            {
                "start_time": "2022-03-20T13:00:00",
                "interval_hours": 2,
                "interval_avg_kwh_price": 1.67,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 80.68,
                "interval_avg_green_energy_percent_estimate": False,
            },
            {
                "start_time": "2022-03-20T14:00:00",
                "interval_hours": 2,
                "interval_avg_kwh_price": 1.98,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 78.18,
                "interval_avg_green_energy_percent_estimate": False,
            },
        ]
        actual_result = self.seas.greenest_interval(2, 2)

        self.assertListEqual(actual_result, expected_result)

    def test_cheapest_1_interval(self):
        """Test the cheapest_interval with interval=1"""
        expected_result = [
            {
                "start_time": "2022-03-20T13:00:00",
                "interval_hours": 1,
                "interval_avg_kwh_price": 1.57,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 85.68,
                "interval_avg_green_energy_percent_estimate": False,
            },
            {
                "start_time": "2022-03-20T14:00:00",
                "interval_hours": 1,
                "interval_avg_kwh_price": 1.77,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 75.68,
                "interval_avg_green_energy_percent_estimate": False,
            },
        ]
        actual_result = self.seas.cheapest_interval(1, 2)

        self.assertListEqual(actual_result, expected_result)

    def test_cheapest_2_interval(self):
        """Test the cheapest_interval with interval=2"""
        expected_result = [
            {
                "start_time": "2022-03-20T13:00:00",
                "interval_hours": 2,
                "interval_avg_kwh_price": 1.67,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 80.68,
                "interval_avg_green_energy_percent_estimate": False,
            },
            {
                "start_time": "2022-03-20T14:00:00",
                "interval_hours": 2,
                "interval_avg_kwh_price": 1.98,
                "interval_avg_kwh_price_estimate": False,
                "interval_avg_green_energy_percent": 78.18,
                "interval_avg_green_energy_percent_estimate": False,
            },
        ]
        actual_result = self.seas.cheapest_interval(2, 2)

        self.assertListEqual(actual_result, expected_result)

    def test_climate_at_timestamp(self):
        """Test the climate_at function, using a timestamp"""
        expected_result = {
            "start_time": "2022-03-20T15:00:00",
            "green_energy_percent": 80.68,
            "co2_intensity": 194,
            "consumption_breakdown_percent": {
                "biomass": 18.64,
                "coal": 16.9,
                "gas": 5.41,
                "geothermal": 0.0,
                "hydro": 13.09,
                "nuclear": 10.02,
                "oil": 0.0,
                "solar": 3.94,
                "wind": 29.99,
                "unknown": 2.0,
            },
        }
        actual_result = self.seas.climate_at("2022-03-20T15:00:00")

        self.assertDictEqual(actual_result, expected_result)

    def test_price_at_timestamp(self):
        """Test the price_at function, using a timestamp"""
        expected_result = {
            "start_time": "2022-03-20T14:00:00",
            "kwh_raw_price": 0.18,
            "kwh_tariffs": 1.59,
            "kwh_total": 1.77,
        }
        actual_result = self.seas.price_at("2022-03-20T14:00:00")

        self.assertDictEqual(actual_result, expected_result)
