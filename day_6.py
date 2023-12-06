import logging
import argparse
from src.logging_args_setup import setup_args
import numpy as np

DAY = "6"


def problem_1(input_file: str) -> None:
    time_lst, dist_lst = parse(input_file)
    out = 1
    for i in range(len(time_lst)):
        time_i = time_lst[i]
        dist_i = dist_lst[i]

        options = np.arange(time_i)
        results = options * time_i - np.square(options)

        n_options = np.sum(results > dist_i)

        logging.debug("On race %i, n_options: %i", i, n_options)

        out = out * n_options

    logging.info("SOln 1 = %i", out)


def problem_2(input_file: str) -> None:
    time_i, dist_i = parse_2(input_file)
    options = np.arange(time_i)
    results = options * time_i - np.square(options)
    n_options = np.sum(results > dist_i)
    logging.info("SOln 2: %i", n_options)


def parse(input_file: str) -> tuple[list[int]]:
    with open(input_file, "r") as f:
        _, rest = f.readline().split(":")
        logging.debug(rest)
        logging.debug(rest.split())
        time_lst = [int(x.strip()) for x in rest.split()]

        _, rest = f.readline().split(":")
        dist_lst = [int(x.strip()) for x in rest.split()]

    return (time_lst, dist_lst)


def parse_2(input_file: str) -> tuple[int]:
    with open(input_file, "r") as f:
        _, rest = f.readline().split(":")
        time_lst = [x.strip() for x in rest.split()]
        time = int("".join(time_lst))

        _, rest = f.readline().split(":")
        dist_lst = [x.strip() for x in rest.split()]
        dist = int("".join(dist_lst))

    return time, dist


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
