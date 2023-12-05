import logging
import argparse
from src.logging_args_setup import setup_args
import numpy as np

DAY = "4"


def parse_card(card_line: str) -> tuple[set[int]]:
    """
    Returns a set of winning numbers, a set of our numbers, and the intersection
    """
    card_and_info = card_line.strip().split(":")
    winning_and_ours = card_and_info[1].strip().split("|")

    winning_nums = set()
    for w in winning_and_ours[0].split():
        winning_nums.add(int(w))

    our_nums = set()
    for o in winning_and_ours[1].split():
        our_nums.add(int(o))

    intersection = winning_nums.intersection(our_nums)
    return (winning_nums, our_nums, intersection)


def problem_1(input_file: str) -> None:
    out = 0
    with open(input_file, "r") as f:
        for l in f:
            w, o, i = parse_card(l)
            if len(i):
                out += 2 ** (len(i) - 1)
    logging.info("SOln: %i", out)


def problem_2(input_file: str) -> None:
    out = 0
    with open(input_file, "r") as f:
        tup_lst = []
        for l in f:
            tup_lst.append(parse_card(l))
        n = len(tup_lst)
        logging.info("N cards: %i", n)

        counter = np.ones(n)
        for i in range(n):
            logging.debug("On card %i", i)
            count_i = counter[i]
            wins_i = len(tup_lst[i][2])
            if wins_i:
                logging.debug("This card has wins %i", wins_i)
                for j in range(1, wins_i + 1):
                    counter[j + i] = counter[j + i] + count_i
                logging.debug("Counter now looks like %s", counter)

    logging.info("Soln 2: %i", counter.sum())


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
