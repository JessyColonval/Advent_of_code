"""
Advent of code - Day 3 (2025)
"""
import sys
import time


def max_and_index(s: str) -> (int, int):
    """
    Find the highest digit in a string.

    Parameters
    ----------
    bank : str
        String where the search will be made.

    Returns
    -------
    (int, int)
        Highest digit value and its index in the string.
    """
    _max = -1
    index = -1
    for i, digit in enumerate(s):
        digit = int(digit)
        if digit > _max:
            _max = digit
            index = i
    return _max, index


def higest_value(s: str, size: int) -> int:
    """
    Finds the largest value in a string.
    The digits are in order, but do not necessarily follow each other.

    Parameters
    ----------
    s : str
        The main string where the search will be made.
    size : int
        The number of digits in the value searched.

    Returns
    -------
    int
        The largest value found.
    """
    # Number of digits to keep at the end of the main string.
    size = -(size - 1)

    result = []
    start = 0
    for i in range(size, 1):
        # End bound of the substring.
        # It is positioned in such a way that there must be as many digits at
        # the end of the main string as are missing to construct the value to
        # be returned.
        # Thus, if the largest number is the last digit of the substring, then
        # there will be enough digits left to complete the value to be
        # constructed.
        end = len(s) + i

        # Substring between 'start' and 'end' bounds.
        sub_s = s[start:end]

        # Finds the higher digit and its index in the substring.
        _max, index = max_and_index(sub_s)

        # Places the new start after the index of the highest value found.
        start += index + 1

        # Appends in the result the value found.
        result.append(f"{_max:d}")

    return int("".join(result))


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    with open(INPUT, 'r', encoding="utf-8") as f:
        banks = [
            line.rstrip()
            for line in f.readlines()
        ]

    FIRST = 0
    SECOND = 0
    for bank in banks:
        FIRST += higest_value(bank, 2)
        SECOND += higest_value(bank, 12)

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}!")
    print(f"The second part solution is {SECOND:d}!")
    print(f"Found in {t:0.5f}s!")
