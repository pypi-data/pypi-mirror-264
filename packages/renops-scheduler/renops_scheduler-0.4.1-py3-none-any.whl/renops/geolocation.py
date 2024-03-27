from typing import Any, Dict, Tuple, Union

import requests

import renops.config as conf


class GeoLocation:
    def __init__(self, location: Union[str, Dict[str, float]] = None):
        self.params = self._get_location_params(location)

    def _get_location_params(self, location: Union[None, str, Dict[str, float]]) -> Dict[str, Any]:
        """
        Returns the parameters based on the provided location (city name or coordinates).
        Args:
            location (Union[str, Dict[str, float]]): The location, either as a string (city name) or as coordinates
                (latitude and longitude). In case None, automatic location detection is executed.
        Returns:
            dict: The parameters for the request.
        """
        auto_synonyms = ["auto", "a", "automatic"]  # Define synomims for word automatic
        if isinstance(location, str) and location not in auto_synonyms:
            # When location is defined as a word
            lat, lon = self._geocode_location(location)
            if conf.runtime.verbose:
                print(f"Location specified: {location}, lat: {lat} lon: {lon}")
        elif location in auto_synonyms:
            # When location is set to auto
            loc = self._get_location()
            if conf.runtime.verbose:
                print(
                    f'Location is set to auto, IP will be used to detect location! found: {loc["city"]},'
                    f' {loc["country"]}'
                )
            lat, lon = loc["loc"].split(",")
        # elif isinstance(location, dict) and "lat" in location and "lon" in location:
        #    lat, lon = location["lat"], location["lon"]
        #    print(f"Location specified: {location}")
        else:
            raise ValueError("Invalid location format")
        return {"lat": lat, "lon": lon}

    def _geocode_location(self, location: str) -> Tuple[float, float]:
        """
        Geocodes the provided location (city name) to obtain latitude and longitude.
        Args:
            location (str): The location (city name) to geocode.
        Returns:
            tuple: The latitude and longitude values.
        """
        headers = {
            'Referer': 'https://renops-api-tango.xlab.si',
            'User-Agent': f'renops-scheduler-user-{conf.user.uuid}'
        }
        response = requests.get(f"{conf.geocoder.url}/search?q={location}&format=json",
                                headers=headers)
        # Check if the API request was successful
        if response.status_code == 200:
            data = response.json()
            # Check if the settlement was found
            if len(data) > 0:
                # Extract the latitude and longitude from the API response
                lat = data[0]["lat"]
                lng = data[0]["lon"]
                return lat, lng
            else:
                print(f'Settlement "{location}" not found.')
                return None, None
        else:
            print(f"API request failed with status code {response.status_code}.")
        return None, None

    def _get_location(self) -> Dict:
        """
        Retrieves the geolocation of the current machine using the 'ipinfo.io' service.

        The method sends a GET request to 'ipinfo.io' which returns a JSON response
        with the IP, city, region, country, and geographic coordinates (latitude and longitude)
        of the machine from where the request was made.
        Returns:
            Dict: A dictionary containing the following keys:
                'ip': The IP address of the machine.
                'city': The city in which the machine is located.
                'region': The region in which the machine is located.
                'country': The country in which the machine is located.
                'loc': The latitude and longitude of the machine's location.
        """

        # Send GET request to 'ipinfo.io' to fetch geolocation data
        response = requests.get(conf.ipinfo.url)
        # Convert the response to JSON and return it
        return response.json()
