import logging
import argparse


def setup_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "-debug", action="store_true", default=False)
    parser.add_argument("-s", "-second", action="store_true", default=False)

    return parser.parse_args()
