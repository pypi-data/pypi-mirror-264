#!/usr/bin/env python3

import argparse
import sys
from argparse import RawTextHelpFormatter

from renops.geoshifter import GeoShift
from renops.scheduler import Scheduler, execute_script
from renops.utils import read_json_from_filename


def main():
    try:
        run()

    except ValueError as error:
        print(f"ValueError: {error}")
        sys.exit(1)  # Exiting with status code 1 signifies an error

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting.")
        sys.exit(0)  # Exiting with status code 0 signifies a clean exit

    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        sys.exit(1)  # Exiting with status code 1 for error


def run():
    print("RUNNING RENOPS SCHEDULER...")
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument("script_path", help="Path to the script to be executed or JSON file in case of geo shifting.")
    parser.add_argument(
            "-l",
            "--location",
            default=None,
            help=(
                "Location can be specified in two ways:\n\n"
                '1. Pass a specific location as a string, e.g., "Berlin, Germany".\n\n'
                "2. Use automatic location detection based on IP address.\n"
                " By using this tag, you agree that your IP can be used to detect your location.\n"
                "You can use any of the following values for this purpose:\n"
                "   -l a (-la)\n"
                "   -l auto\n"
                "   -l automatic\n"
            )
        )
    parser.add_argument("-gs",
                        "--geo-shift",
                        action="store_true",
                        help="JSON on given path should be formated as:\n"
                        "{\n"
                        "  \"hpc1\": {\n"
                        "    \"location\": \"Berlin, Germany\",\n"
                        "    \"cmd\": \"ssh user@hpc1 python3 train.py\"\n"
                        "  },\n"
                        "  \"hpc2\": {\n"
                        "    \"location\": \"Madrid, Spain\",\n"
                        "    \"cmd\": \"ssh user@hpc2 python3 train.py\"\n"
                        "  },\n"
                        "  \"hpc3\": {\n"
                        "    \"location\": \"Copenhagen, Denmark\",\n"
                        "    \"cmd\": \"ssh user@hpc3 python3 train.py\"\n"
                        "  }\n"
                        "}")
    parser.add_argument("-op",
                        "--optimise-price",
                        action="store_true",
                        help="Optimise for energy price.")
    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        help="Verbose mode.")
    parser.add_argument("-r",
                        "--runtime",
                        type=int,
                        default=None,
                        help="Runtime in hours. (Not for geo shift mode)")
    parser.add_argument(
            "-d",
            "--deadline",
            type=int,
            default=120,
            help="Deadline in hours, by when should script finish running (Not for geo shift mode)", # noqa
        )
    args = parser.parse_args()

    if args.optimise_price:
        print("Optimising for price! (Day-ahead forecast only)")
    if args.geo_shift:
        print("Geo shift mode specified, shifting in space...")
        if not args.script_path.endswith(".json"):
            raise ValueError("The input file must be a JSON file.")

        s = GeoShift(
            locations=read_json_from_filename(args.script_path),
            optimise_price=args.optimise_price,
            verbose=args.verbose,
        )
        s.shift()
    elif args.location:
        print("Location specified, shifting in time...")
        args = parser.parse_args()

        if not args.runtime:
            print("Runtime not specified, using default setting of 3 hours!")
            args.runtime = 3

        s = Scheduler(
            deadline=args.deadline,
            runtime=args.runtime,
            location=args.location,
            optimise_price=args.optimise_price,
            verbose=args.verbose,
            action=execute_script,
            argument=([args.script_path]),
        )
        s.run()
    else:
        raise ValueError("Specifiy either location (-l) or geo shift mode (-gs). Check --help for more details.") # noqa


if __name__ == "__main__":
    main()
