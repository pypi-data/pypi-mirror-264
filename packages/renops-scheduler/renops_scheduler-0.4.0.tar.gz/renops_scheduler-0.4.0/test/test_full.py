import unittest

from renops.geoshifter import GeoShift
from renops.scheduler import Scheduler


class SchedulerTests(unittest.TestCase):
    def setUp(self):
        # Create a Scheduler instance with sample parameters
        self.scheduler = Scheduler(
            deadline=24,
            runtime=8,
            location="Kranj",
            action=lambda: print("Executing action"),
            verbose=True,
            optimise_price=False,
            argument=(1, 2, 3),
            kwargs={"key": "value"}
        )
        self.data = self.scheduler.get_data()

    def test_get_data(self):
        # Test the get_data method
        self.assertFalse(self.data.isna().any().any())

    def test_preprocess_data(self):
        # Test the _preprocess_data method
        preprocessed_data = self.scheduler._preprocess_data(self.data)
        self.assertIsNotNone(preprocessed_data)
        # Add more assertions based on the expected behavior of the method


class GeoShiftTests(unittest.TestCase):
    def setUp(self):
        # Create a GeoShift instance with sample parameters
        self.locations = {
            "Location1": {"location": "Berlin", "cmd": "echo 'Hello, Berlin!'"},
            "Location2": {"location": "Paris", "cmd": "echo 'Bonjour, Paris!'"},

        }
        self.geoshifter = GeoShift(
            locations=self.locations,
            optimise_price=True,
            verbose=True
        )

    def test_check_subkeys(self):
        # Test the check_subkeys method
        self.assertTrue(self.geoshifter.check_subkeys(self.locations))
        # Add more assertions based on the expected behavior of the method

    def test_shift(self):
        # Test the shift method
        stdout, stderr = self.geoshifter.shift()
        self.assertIsNotNone(stdout)
        self.assertEqual(stderr, "")
        # Add more assertions based on the expected behavior of the method


if __name__ == '__main__':
    unittest.main()
