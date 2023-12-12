import logging
import argparse
from src.logging_args_setup import setup_args
import numpy as np

DAY = "9"

DIFF_FILTER = np.array([1, -1])


def find_prediction(a: np.array, second_part: bool = False) -> int:
    result_lst = [a]
    c = a
    c_post = np.convolve(a, DIFF_FILTER, mode="valid")
    while not np.allclose(np.zeros_like(c), c):
        # logging.debug("c_pre: %s", c)
        c_post = np.convolve(c, DIFF_FILTER, mode="valid")
        logging.debug("c_post: %s", c_post)
        result_lst.append(c_post)

        c = c_post

    o = []
    for i, z in enumerate(result_lst):
        if second_part:
            o.append(z[0] * ((-1) ** i))
        else:
            o.append(z[-1])

    return np.sum(o)


def problem_1(input_file: str) -> None:
    out = 0
    with open(input_file, "r") as f:
        for l in f:
            logging.debug("############## New line")
            a = np.array([int(x) for x in l.split()])
            logging.debug("a = %s", a)

            pred = find_prediction(a)

            logging.debug("Pred = %i", pred)

            out += pred

        logging.info("Soln 1 = %i", out)


def problem_2(input_file: str) -> None:
    out = 0
    with open(input_file, "r") as f:
        for l in f:
            logging.debug("############## New line")
            a = np.array([int(x) for x in l.split()])
            logging.debug("a = %s", a)

            pred = find_prediction(a, second_part=True)

            logging.debug("Pred = %i", pred)

            out += pred

        logging.info("Soln 1 = %i", out)


def main(a: argparse.Namespace) -> None:
    if a.d:
        fp_1 = f"inputs/{DAY}_1_debug.txt"
        fp_2 = f"inputs/{DAY}_1_debug.txt"

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
