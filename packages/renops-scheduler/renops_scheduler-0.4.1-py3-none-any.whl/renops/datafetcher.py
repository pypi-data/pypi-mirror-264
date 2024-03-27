import sys
from typing import Dict, List, Union

import pandas as pd
import requests

import renops.config as conf
from renops.geolocation import GeoLocation


class DataFetcher:
    def __init__(self, location: Union[str, Dict[str, float]] = None):
        """
        Initialize the DataFetcher class.
        Args:
            url (str): The URL of the server.
            location (Union[str, Dict[str, float]]): The location, either as a string (city name) or as coordinates
                (latitude and longitude).
        """
        self.params = GeoLocation(location).params

    def filter_dict(self, in_dict: Dict, keys_to_keep: List) -> Dict:
        """
        Return dictionary with keys we want to keep
        """
        return {key: in_dict[key] for key in keys_to_keep}

    def _request_data(self, url: str) -> Dict:
        response = requests.get(
                url, params=self.params, headers={"key": conf.renopsapi.key}
            )
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes

        return response.json()

    def _preporcess_data(self, response: Dict) -> pd.DataFrame:
        # Define needed keys for calculating renewable potential
        keys_to_keep = ["timestamps_hourly", "metric"]

        # Keep just the keys we need
        data = self.filter_dict(response, keys_to_keep)

        # Convert to DataFrame
        data = pd.DataFrame(data)

        # Get timestamp units
        unit = response["units"]["timestamps_hourly"]

        # Convert epoch strings to epoch ints
        data["epoch"] = data["timestamps_hourly"].astype(int)

        # Convert to datetime
        data["Date"] = pd.to_datetime(data["epoch"], unit=unit)
        data.set_index("Date", inplace=True)

        return data

    def fetch_renewable_potential(self) -> Dict:
        """
        Fetches the renewable potential data for the next 5 days.
        Returns:
            dict or None: The fetched data as a JSON object, or None if an error occurred.
        """
        # Get reponse
        response = self._request_data(conf.renopsapi.renewable_potential)

        # Rename columns
        response["metric"] = response["renewable_potential_forecast_hourly"]

        return response

    def fetch_prices(self) -> Dict:
        """
        Fetches day ahead prices.
        Returns:
            dict or None: The fetched data as a JSON object, or None if an error occurred.
        """
        # Get reponse
        response = self._request_data(conf.renopsapi.price)

        # Rename columns
        response["metric"] = response["day_ahead_prices"]

        return response

    def fetch(self, optimise_price):
        try:
            if optimise_price:
                response = self.fetch_prices()
            else:
                response = self.fetch_renewable_potential()
            return self._preporcess_data(response)

        except requests.exceptions.RequestException as e:
            print("Error occurred:", str(e))
            if "422" in str(e):
                print(
                    "Could not map a bidding zone to given coordinate. "
                    "Check (https://www.entsoe.eu/network_codes/bzr/) for more details."
                    )
            sys.exit(1)
