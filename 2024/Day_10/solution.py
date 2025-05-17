"""
Advent of code - Day 10 (2024)
"""
from typing import List, Dict
import os
import sys
import time
from collections import deque
sys.path.append(os.path.abspath("../.."))

from reader import csv_to_list

# All directions accessible from any point as a complex number:
# -1 for left;
# 1 for right;
# -1j for up;
# 1j for down.
DIRECTIONS = [-1, 1, -1j, 1j]

# The maximum height.
PEAK = 9


def find_trailheads(topo_map: Dict[complex, int]) -> List[complex]:
    """
    Find all the trailheads (places where the height is zero).

    Parameters
    ----------
    topo_map: Dict[complex, int]
        A topographical map as a dictionary that associates each position as a
        complex number with a height.

    Return
    ------
    List[complex]
        list of trailhead positions.
    """
    return [
        pos for pos, height in topo_map.items()
        if height == 0
    ]


def get_score(trailhead: complex,
              topo_map: Dict[complex, int],
              part: int = 1) -> int:
    """
    Computes the number of different paths from a starting point (height 0) to
    a peak (height 9).

    Parameters
    ----------
    trailhead: complex
        The position of a trailhead.
    topo_map: Dict[complex, int]
        A topographical map as a dictionary that associates each position as a
        complex number with a height.
    part: int
        The part of the puzzle to solve (1 or 2).

    Return
    ------
    int
        the number of different paths.
    """
    if part not in (1, 2):
        raise ValueError("Unknown puzzle part number!")

    # Create a stack containing the trail from a starting point (trailhead).
    trails = deque([trailhead])

    score = 0
    visited = set()
    while trails:
        # Gets the last explored position from the stack and remove it.
        current = trails.pop()

        # Increment the score if the last position is a peak (height to 9).
        if topo_map[current] == PEAK:
            score += 1
            continue

        # Iterates all possible directions.
        for offset in DIRECTIONS:
            # Computes the next position of the trail according the current
            # position.
            new_position = current + offset

            # If we are solving the first part of the puzzle and this position
            # has already been visited, we move on to the next direction
            # without doing anything.
            if part == 1 and new_position in visited:
                continue

            # Adds this new position to those already visited and to the trail
            # if there is a +1 height difference.
            if topo_map.get(new_position) == topo_map[current] + 1:
                trails.append(new_position)
                visited.add(new_position)
    return score


def solve(trailheads: List[complex],
          topo_map: Dict[complex, int],
          part: int = 1) -> int:
    """
    Computes the total puzzle score.

    Parameters
    ----------
    trailheads: List[complex]
        The position of all existed trailheads.
    topo_map: Dict[complex, int]
        A topographical map as a dictionary that associates each position as a
        complex number with a height.
    part: int
        The part of the puzzle to solve (1 or 2).

    Return
    ------
    int
        total puzzle score.
    """
    return sum(
        get_score(trailhead, topo_map, part)
        for trailhead in trailheads
    )


if __name__ == "__main__":
    FILE_NAME = sys.argv[1]

    t = time.time()

    # Gets the input puzzle as 2D array of intergers.
    data = csv_to_list(FILE_NAME, None, "row")

    # Converts the input puzzle as a dict of position (as a complex number)
    # and the height at this point.
    maps = {
        complex(i, j): height
        for i, row in enumerate(data)
        for j, height in enumerate(row)
    }

    # Find all trailheads.
    trailheads = find_trailheads(maps)

    # Solve the two parts of the puzzle.
    FIRST = solve(trailheads, maps, 1)
    SECOND = solve(trailheads, maps, 2)

    t = time.time() - t

    print(f"The first part result is {FIRST:d}.")
    print(f"The second part result is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
