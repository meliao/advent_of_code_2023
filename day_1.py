def problem_1() -> None:
    total_val = 0
    with open("inputs/1_1.txt", "r") as f:
        for l in f:
            str_len = len(l)

            for i in range(str_len):
                if l[i].isdigit():
                    first_digit = 10 * int(l[i])
                    break

            for i in range(str_len - 1, -1, -1):
                if l[i].isdigit():
                    last_digit = int(l[i])
                    break

            str_val = first_digit + last_digit

            total_val += str_val
    print(total_val)


NUM_DD = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "zero": "0",
}


def line_to_lst_of_numbers(x: str) -> list:
    # print(x)
    l = len(x)

    y = [None] * len(x)

    for k in NUM_DD.keys():
        idx = 0
        f_idx = x.find(k, idx)
        if f_idx > -1:
            y[f_idx] = int(NUM_DD[k])
        while f_idx > -1:
            f_idx = x.find(k, f_idx + 1)
            if f_idx > -1:
                y[f_idx] = int(NUM_DD[k])

    for i in range(l):
        if x[i].isdigit():
            y[i] = int(x[i])

    return y


def problem_2() -> None:
    total_val = 0
    with open("inputs/1_1.txt", "r") as f:
        for l in f:
            # print(l)
            y = line_to_lst_of_numbers(l)
            # print(y)

            str_len = len(y)

            for i in range(str_len):
                if isinstance(y[i], int):
                    first_digit = 10 * y[i]
                    break

            for i in range(str_len - 1, -1, -1):
                if isinstance(y[i], int):
                    last_digit = int(y[i])
                    break

            str_val = first_digit + last_digit
            # print(str_val)

            total_val += str_val
    print(total_val)


def main() -> None:
    # problem_1()
    problem_2()


if __name__ == "__main__":
    main()
