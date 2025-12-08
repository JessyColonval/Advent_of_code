"""
Advent of code - Day 4 (2025)
"""
from typing import List
import sys
import time


# The 8 directions to consider.
DIRECTIONS = [
    tuple([i, j])
    for i in (-1, 0, 1)
    for j in (-1, 0, 1)
    if not (i == 0 and j == 0)
]


def n_rolls(_map: List[List[str]], x: int, y: int, paper: str = '@') -> int:
    """
    Count the number of rolls of paper in the 8 adjacent cells.

    Parameters
    ----------
    _map : List[int]
        Complete map of the rolls.
    x : int
        X coordinate of the starting cell.
    y : int
        Y coordinate of the starting cell.
    paper : str, default: '@'
        Character representing a roll in the given map.

    Returns
    -------
    int
        Number of rolls paper found.
    """
    n_lines = len(_map)
    n_cols = len(_map[x])

    result = 0
    for h, v in DIRECTIONS:
        x0 = x + h
        y0 = y + v
        if 0 <= x0 < n_lines and 0 <= y0 < n_cols and _map[x0][y0] == paper:
            result += 1

    return result


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    # Reads the input file and constructs the paper roll map.
    with open(INPUT, 'r', encoding="utf-8") as f:
        _map = [
            list(line.rstrip())
            for line in f.readlines()
        ]

    # Character representing a roll.
    PAPER = '@'

    FIRST = 0
    SECOND = 0
    N_ITER = 0
    FOUND = True
    while FOUND:
        indices = []
        for i, line in enumerate(_map):
            for j, e in enumerate(line):
                if e == PAPER and n_rolls(_map, i, j, PAPER) < 4:
                    # Count the number of paper rolls that are adjacent to less
                    # than 4 other rolls.
                    # Keep this number for the first iteration for the first
                    # part of this puzzle.
                    if N_ITER == 0:
                        FIRST += 1
                    SECOND += 1

                    # Keep the indices of these rolls.
                    indices.append((i, j))

        # Check if any rolls were found to continue the loop or not.
        FOUND = len(indices) > 0

        # Removes all found rolls from the map.
        # This must only be done after the research has been completed so as
        # not to influence the findings.
        for i, j in indices:
            _map[i][j] = '.'

        N_ITER += 1

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
