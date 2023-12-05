import logging
import argparse
from src.logging_args_setup import setup_args

DAY = ""


def problem_1(input_file: str) -> None:
    with open(input_file, "r") as f:
        for l in f:
            pass


def problem_2(input_file: str) -> None:
    with open(input_file, "r") as f:
        for l in f:
            pass


def main(a: argparse.Namespace) -> None:
    if a.d:
        fp_1 = f"inputs/{DAY}_1_debug.txt"
        fp_2 = f"inputs/{DAY}_2_debug.txt"

    else:
        fp_1 = f"inputs/{DAY}_1.txt"
        fp_2 = f"inputs/{DAY}_1.txt"

    if a.s:
        problem_2(fp_2)
    else:
        problem_1(fp_1)


if __name__ == "__main__":
    a = setup_args()

    if a.d:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    main(a)
