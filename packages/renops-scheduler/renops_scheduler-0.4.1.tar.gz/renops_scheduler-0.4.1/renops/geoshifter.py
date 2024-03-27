import time

from renops.datafetcher import DataFetcher
from renops.utils import execute_linux_command, get_closest_metric


class GeoShift:
    def __init__(self,
                 locations: dict,
                 optimise_price: bool = False,
                 verbose: bool = False):
        self.locations = locations
        self.optimise_price = optimise_price
        self.verbose = verbose

    def check_subkeys(self, dictionary: dict) -> bool:
        for key, value in dictionary.items():
            if 'location' not in value or 'cmd' not in value:
                return False
        return True

    def shift(self):
        if not self.check_subkeys(self.locations):
            raise ValueError('Each dictionary in the input dictionary must have a "location" and "cmd" key.')

        metrics = {}
        for key, value in self.locations.items():
            current_epoch = int(time.time())
            forecast = DataFetcher(value['location']).fetch(optimise_price=self.optimise_price)
            current_metric = get_closest_metric(forecast, current_epoch)
            if self.verbose:
                print(f"Current metric for {key} in {value['location']} is: {current_metric}")
            metrics[key] = current_metric

        if self.optimise_price:
            best_location = min(metrics, key=metrics.get)
        else:
            best_location = max(metrics, key=metrics.get)
        ep = self.locations[best_location]

        print(f'Found optimal location: {best_location}, {ep["location"]}!')
        print(f"... Running specified command: {ep['cmd']}!")

        stdout, stderr = execute_linux_command(ep['cmd'])
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")

        return stdout, stderr
