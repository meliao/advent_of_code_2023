import logging
import argparse
from src.logging_args_setup import setup_args

DAY = "2"


def problem_1(input_file: str) -> None:
    target_blue = 14
    target_green = 13
    target_red = 12

    out = 0
    with open(input_file, "r") as f:
        for l in f:
            logging.debug("##############")
            logging.debug(l)
            max_blue = 0
            max_red = 0
            max_green = 0
            x = l.split(":")
            game_id = int(x[0].split()[-1])
            game_lst = x[1].split(";")
            for g in game_lst:
                trial_lst = g.split(",")
                for t in trial_lst:
                    # logging.debug("t: %s", t)
                    if t.endswith("red"):
                        max_red = max(max_red, int(t.split()[0]))
                    if t.endswith("blue"):
                        max_blue = max(max_blue, int(t.split()[0]))
                    if t.endswith("green"):
                        max_green = max(max_green, int(t.split()[0]))

                    # logging.debug(
                    #     "max_blue %s, max_green: %s, max_red: %s",
                    #     max_blue,
                    #     max_green,
                    #     max_red,
                    # )
            if (
                (max_blue <= target_blue)
                and (max_red <= target_red)
                and (max_green <= target_green)
            ):
                logging.debug("Game %i is valid", game_id)
                out += game_id

    logging.info("Problem 1 soln: %i", out)


def problem_2(input_file: str) -> None:
    out = 0
    with open(input_file, "r") as f:
        for l in f:
            logging.debug("##############")
            logging.debug(l)
            min_blue = 0
            min_red = 0
            min_green = 0
            x = l.split(":")
            game_id = int(x[0].split()[-1])
            game_lst = x[1].split(";")
            for g in game_lst:
                trial_lst = g.split(",")
                logging.debug("trial_lst: %s", trial_lst)
                for t in trial_lst:
                    # logging.debug("t: %s", t)
                    t = t.strip()
                    if t.endswith("red"):
                        min_red = max(min_red, int(t.split()[0]))
                    if t.endswith("blue"):
                        min_blue = max(min_blue, int(t.split()[0]))
                    if t.endswith("green"):
                        min_green = max(min_green, int(t.split()[0]))

            logging.debug(
                "Min_blue: %i, min_red: %i, min_green: %i", min_blue, min_red, min_green
            )
            set_prod = min_red * min_blue * min_green
            logging.debug("Set prod: %i", set_prod)
            out += set_prod
    logging.info("Problem 2 soln: %i", out)


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
