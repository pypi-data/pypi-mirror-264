import argparse
from argparse import Namespace


def parse_args() -> Namespace:
    """
    Parses command-line arguments.

    Returns:
        Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario_id", help="Id of the scenario", type=int, required=False
    )
    return parser.parse_args()
