import logging
import argparse
from src.logging_args_setup import setup_args
import numpy as np

DAY = "3"


def find_symbols_and_digits(x: np.ndarray) -> np.ndarray:
    digit_arr = np.char.isdigit(x)
    symbol_arr = x == "."
    # return np.logical_not(symbol_arr), digit_arr

    return np.logical_not(np.logical_or(digit_arr, symbol_arr)), digit_arr


def extract_idx_from_row(x: np.ndarray):
    """For each integer that appears in the row, this returns starting_idx,
    number of digits, and integer value"""
    n = len(x)
    i = 0
    currently_in_int = False
    out_lst = []
    while i < n:
        if x[i].isdigit():
            if not currently_in_int:
                out_lst.append([i, 1, x[i]])
            else:
                out_lst[-1][1] += 1
                out_lst[-1][2] += x[i]

            currently_in_int = True
        else:
            currently_in_int = False
        i += 1
    return out_lst


def check_if_int_adjacent(start_idx_0, start_idx_1, int_len, symbols_bool_arr) -> bool:
    logging.debug(f"check_if_int, input {start_idx_0}, {start_idx_1}, {int_len}")
    n, p = symbols_bool_arr.shape

    min_0 = max(0, start_idx_0 - 1)
    max_0 = min(n, start_idx_0 + 2)

    min_1 = max(0, start_idx_1 - 1)
    max_1 = min(p, start_idx_1 + 1 + int_len)

    sub_arr = symbols_bool_arr[min_0:max_0, min_1:max_1]
    logging.debug(f"check_if_int, sub_arr shape {sub_arr.shape}")

    return np.any(sub_arr)


def problem_1(input_file: str) -> None:
    lines = np.genfromtxt(input_file, dtype="str", delimiter="\n", comments=None)
    out = 0

    # Determine the maximum length of a line to create a 2D character array
    max_line_length = max(len(line) for line in lines)
    f_arr = np.array([list(line.ljust(max_line_length)) for line in lines])
    logging.debug(f_arr)
    logging.info(f_arr.shape)
    f_symbols, f_digits = find_symbols_and_digits(f_arr)
    logging.debug(f_symbols)

    for i, row in enumerate(f_arr):
        ints_in_row = extract_idx_from_row(row)
        for x in ints_in_row:
            if check_if_int_adjacent(i, x[0], x[1], f_symbols):
                logging.debug("Int %s is good", x[2])
                out += int(x[2])
            else:
                logging.debug("Int %s is not good", x[2])
    logging.info(out)


def extract_int_from_idx(f_arr: np.ndarray, idx_0: int, idx_1: int):
    idx_1_upper = idx_1
    idx_1_lower = idx_1
    n, p = f_arr.shape
    while f_arr[idx_0, idx_1_upper].isdigit():
        idx_1_upper += 1
        if idx_1_upper == n:
            break

    while f_arr[idx_0, idx_1_lower].isdigit():
        idx_1_lower -= 1
        if idx_1_lower == -1:
            break
    int_arr = f_arr[idx_0, idx_1_lower + 1 : idx_1_upper]
    # logging.debug("extract_int_from_idx: int_arr: %s", int_arr)
    return "".join([x for x in int_arr])


def read_digits_in(input_file: str) -> None:
    lines = np.genfromtxt(input_file, dtype="str", delimiter="\n", comments=None)
    max_line_length = max(len(line) for line in lines)
    f_arr = np.array(
        [list(line.ljust(max_line_length)) for line in lines], dtype="object"
    )
    f_arr_out = np.copy(f_arr)
    n, p = f_arr.shape
    for i in range(n):
        for j in range(p):
            if f_arr[i, j].isdigit():
                f_arr_out[i, j] = extract_int_from_idx(f_arr, i, j)

    return f_arr_out


def find_gear_ratio(arr: np.ndarray) -> int:
    logging.debug("find_gear_ratio: arr: %s", arr)
    digits = np.empty(arr.shape, dtype=np.int32)
    n, p = arr.shape
    for i in range(n):
        for j in range(p):
            if arr[i, j].isdigit():
                digits[i, j] = int(arr[i, j])
            else:
                digits[i, j] = 0
    logging.debug("find_gear_ratio: digits: %s", digits)

    # First check whether there are 3 unique vals in digits
    unique_digits = np.sort(np.unique(digits))
    if len(unique_digits) == 3:
        return unique_digits[1] * unique_digits[2]

    # Edge cases where the same digit may appear in 2 places
    elif len(unique_digits) == 2:
        return 0
    else:
        return 0


def problem_2(input_file: str) -> None:
    f_arr = read_digits_in(input_file)

    out = 0

    # Determine the maximum length of a line to create a 2D character array
    logging.info(f_arr.shape)
    logging.debug(f_arr)
    star_locs = np.argwhere(f_arr == "*")
    logging.debug(star_locs)
    logging.debug(star_locs.shape)
    for loc in star_locs:
        out += find_gear_ratio(f_arr[loc[0] - 1 : loc[0] + 2, loc[1] - 1 : loc[1] + 2])
    logging.info(out)


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
