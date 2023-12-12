import logging
import argparse
from src.logging_args_setup import setup_args
import numpy as np

DAY = "7"

CARD_LST = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
CARD_LST.reverse()
CARD_LST_2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
CARD_LST_2.reverse()


def parse_hand(s: str, second_part: bool = False) -> tuple[list[str], int]:
    cards, bet = s.split()
    if second_part:
        cards_lst = [CARD_LST_2.index(x) for x in cards]
    else:
        cards_lst = [CARD_LST.index(x) for x in cards]

    bet_int = int(bet)
    return cards_lst, bet_int


def score_hand(card_lst: list[str], second_part: bool = False) -> int:
    """
    This way when we sort, hand type is most important, then first card,
    then second, so on...
    """
    if second_part:
        hand_type = find_hand_type_2(card_lst)
    else:
        hand_type = find_hand_type(card_lst)
    logging.debug("score_hand: hand is %s, and hand_type is %i", card_lst, hand_type)
    out = 0
    len_card_lst = 5
    for i in range(len_card_lst):
        out += (13 ** (len_card_lst - i - 1)) * int(card_lst[i])
    out += (13**5) * hand_type

    return out


def find_hand_type_2(card_lst: list[int]) -> int:
    """6 for 5 of a kind
    5 for 4 of a kind
    4 for full house
    3 for 3 of a kind
    2 for 2 pair
    1 for pair
    0 otherwise

    J (index 0) are wild
    """
    card_lst_without_j = [x for x in card_lst if x != 0]

    num_j_cards = len(card_lst) - len(card_lst_without_j)
    # logging.debug("find_hand_type_2: hand: %s, has %i jokers", card_lst, num_j_cards)

    if num_j_cards == 0:
        return find_hand_type(card_lst)
    elif num_j_cards == 5:
        return 6

    u = np.unique(card_lst_without_j)
    l = len(u)
    counts = [card_lst_without_j.count(x) for x in u]

    if l == 1:
        # Jokers become the only other card present and we have 5 of a kind
        out = 6

    elif l == 2:
        if np.min(counts) == 1:
            # Only 1 other card, so we can get 4 of a kind
            out = 5
        else:
            # Otherwise, full house is possible.
            out = 4

    elif l == 3:
        # This has to be of pattern A B C A J, which means 3 of a kind is possible.
        out = 3

    else:
        # l == 4 in this case. Pattern A B C D J, pair is highest possible.
        out = 1

    return out


def find_hand_type(card_lst: list[int]) -> int:
    """6 for 5 of a kind
    5 for 4 of a kind
    4 for full house
    3 for 3 of a kind
    2 for 2 pair
    1 for pair
    0 otherwise
    """

    u = np.unique(card_lst)
    l = len(u)
    if l == 1:
        out = 6
    elif l == 2:
        # This could be 4 of a kind or full house
        if card_lst.count(u[0]) == 4 or card_lst.count(u[1]) == 4:
            out = 5
        else:
            out = 4
    elif l == 3:
        # This could be 3 of a kind of 2 pair
        counts = [card_lst.count(x) for x in u]
        if max(counts) == 3:
            out = 3
        else:
            out = 2

    elif l == 4:
        # One pair
        out = 1
    else:
        # High card
        out = 0
    return out


def problem_1(input_file: str) -> None:
    bet_lst = []
    score_lst = []
    with open(input_file, "r") as f:
        for l in f:
            card_lst_l, bet_l = parse_hand(l)
            # logging.debug("Card_lst: %s, bet: %i", card_lst_l, bet_l)
            hand_score = score_hand(card_lst_l)
            logging.debug("hand_score: %i", hand_score)

            bet_lst.append(bet_l)
            score_lst.append(hand_score)

    logging.info("Parsed %i, %i cards", len(bet_lst), len(score_lst))
    logging.info("%i unique scores", np.unique(score_lst).shape[0])

    score_arr = np.array(score_lst)
    sorting = np.argsort(score_arr)
    ranking = np.argsort(sorting) + 1
    logging.debug("Here's the sorting of the hands: %s", sorting)
    logging.debug("Here's the sorted scores: %s", score_arr[sorting])
    logging.debug("Here's the ranking: %s", ranking)
    total_score = np.sum(np.array(bet_lst) * ranking)
    logging.info("Total score: %i", total_score)


def problem_2(input_file: str) -> None:
    bet_lst = []
    score_lst = []
    with open(input_file, "r") as f:
        for l in f:
            card_lst_l, bet_l = parse_hand(l, second_part=True)
            # logging.debug("Card_lst: %s, bet: %i", card_lst_l, bet_l)
            hand_score = score_hand(card_lst_l, second_part=True)
            # logging.debug("hand_score: %i", hand_score)

            bet_lst.append(bet_l)
            score_lst.append(hand_score)
    logging.info("Parsed %i, %i cards", len(bet_lst), len(score_lst))
    logging.info("%i unique scores", np.unique(score_lst).shape[0])

    score_arr = np.array(score_lst)
    sorting = np.argsort(score_arr)
    ranking = np.argsort(sorting) + 1
    logging.debug("Here's the sorting of the hands: %s", sorting)
    logging.debug("Here's the sorted scores: %s", score_arr[sorting])
    logging.debug("Here's the ranking: %s", ranking)
    total_score = np.sum(np.array(bet_lst) * ranking)
    logging.info("Total score: %i", total_score)


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
