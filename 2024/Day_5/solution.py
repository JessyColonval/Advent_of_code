"""
Advent of code - Day 5
"""
import re
import sys
import time
from typing import Any
from collections.abc import Sequence, Mapping


def is_one_page_order_respected(rules: Mapping[int, Mapping[int, int]],
                                order: Sequence[int],
                                start: int) -> bool:
    """
    Checks that a page is correctly ordered according to a set of given rules.

    Parameters
    ----------
    rules: Mapping[int, Mapping[int, int]]
        Ordering rules that pages must respect.
        Each page number is associated with a map that indicates if the other
        page numbers must be located before (-1) or after (1) it.
    order: Sequence[int]
        An ordered page list.
    start: int
        Page index to check.

    Returns
    -------
    bool
        Returns true if the page is well-ordered, false otherwise.
    """
    page = order[start]
    return all(
        rules[page][order[i]] == 1 if i > start
        else rules[page][order[i]] == -1 if i < start
        else True
        for i in range(0, len(order))
    )


def is_order_respected(rules: Mapping[int, Mapping[int, int]],
                       order: Sequence[int]) -> bool:
    """
    Checks that a set of page numbers is correctly ordered according to set of
    given rules.

    Parameters
    ----------
    rules: Mapping[int, Mapping[int, int]]
        Ordering rules that pages must respect.
        Each page number is associated with a map that indicates if the other
        page numbers must be located before (-1) or after (1) it.
    order: Sequence[int]
        An ordered page list.

    Returns
    -------
    bool
        Returns true if the set of page is well-ordered, false otherwise.
    """
    return all(
        is_one_page_order_respected(rules, order, i)
        for i in range(0, len(order))
    )


def swap(order: Sequence[Any], i: int, j: int) -> None:
    """
    Swap two elements in a given list.

    Parameters
    ----------
    order: Sequence[Any]
        The list in which these elements are swapped.
    i: int
        First element index.
    j: int
        Second element index.

    Raises
    ------
    ValueError
        when i or j is outside the list boundaries.
    """
    if i < 0 or i >= len(order):
        raise ValueError("The index of the first element is outside the list.")
    if j < 0 or j >= len(order):
        raise ValueError("The index of the second element is outside the list")
    tmp = order[i]
    order[i] = order[j]
    order[j] = tmp


def index_missplace_right(rules: Mapping[int, Mapping[int, int]],
                          order: Sequence[int],
                          start: int) -> int:
    """
    Returns the first page number index encountered after the given page number
    when it should have been before.

    Parameters
    ----------
    rules: Mapping[int, Mapping[int, int]]
        Ordering rules that pages must respect.
        Each page number is associated with a map that indicates if the other
        page numbers must be located before (-1) or after (1) it.
    order: Sequence[int]
        An ordered page list.
    start: int
        Page index to check.

    Returns
    -------
    int
        the page index or -1 if none is found.
    """
    page = order[start]
    for i in range(start+1, len(order)):
        if rules[page][order[i]] == -1:
            return i
    return -1


def index_missplace_left(rules: Mapping[int, Mapping[int, int]],
                         order: Sequence[int],
                         start: int) -> int:
    """
    Returns the first page number index encountered before the given page
    number when it should have been after.

    Parameters
    ----------
    rules: Mapping[int, Mapping[int, int]]
        Ordering rules that pages must respect.
        Each page number is associated with a map that indicates if the other
        page numbers must be located before (-1) or after (1) it.
    order: Sequence[int]
        An ordered page list.
    start: int
        Page index to check.

    Returns
    -------
    int
        the page index or -1 if none is found.
    """
    page = order[start]
    for i in range(0, start):
        if rules[page][order[i]] == 1:
            return i
    return -1


def reorganize(rules: Mapping[int, Mapping[int, int]],
               order: Sequence[int]) -> None:
    """
    Reorganizes a list of page numbers so that it is correctly ordered.

    Parameters
    ----------
    rules: Mapping[int, Mapping[int, int]]
        Ordering rules that pages must respect.
        Each page number is associated with a map that indicates if the other
        page numbers must be located before (-1) or after (1) it.
    order: Sequence[int]
        An ordered page list.
    """
    while not is_order_respected(rules, order):
        for i in range(0, len(order)):
            j = index_missplace_right(rules, order, i)
            if j != -1:
                swap(order, i, j)
        for i in range(0, len(order)):
            j = index_missplace_left(rules, order, i)
            if j != -1:
                swap(order, i, j)


if __name__ == "__main__":
    FILE_NAME = sys.argv[1]

    t = time.time()

    orders = []
    rules = {}
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        for line in f.readlines():
            # Check if the current line has the format of a new rule.
            if re.search(r"^[1-9][0-9]+\|[1-9][0-9]+$", line):
                pages = line.split("|")

                # Gets the two pages numbers
                previous = int(pages[0])
                follow = int(pages[1])

                # Creates a mapping if the two pages aren't already present.
                if previous not in rules:
                    rules[previous] = {}
                if follow not in rules:
                    rules[follow] = {}

                rules[previous][follow] = 1
                rules[follow][previous] = -1

            elif re.search("^([1-9][0-9]+,)+[1-9][0-9]+$", line):
                pages = line.split(',')
                orders.append([int(page) for page in pages])

    # First part.
    first = sum(
        order[len(order)//2] if is_order_respected(rules, order) else 0
        for order in orders
    )

    # Second part.
    indices = []  # Indices for sets of misordered pages
    for i in range(0, len(orders)):
        if not is_order_respected(rules, orders[i]):
            reorganize(rules, orders[i])
            indices.append(i)

    second = sum(
        orders[i][len(orders[i])//2]
        for i in indices
    )

    t = time.time() - t

    print(f"The first part result is {first:d}.")
    print(f"The second part result is {second:d}.")
    print(f"Found in {t:.5f}s!")
