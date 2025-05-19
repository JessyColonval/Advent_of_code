"""
Advent of code - Day 11 (2024)
"""
from typing import List, Dict
import re
import sys
import time
from functools import cache


@cache
def change(stone: str) -> List[str]:
    """
    Calculates all the stones produced by a starting stone after a blink.
    Caches the results of stones produced, to avoid recalculating them when the
    function encounters the same starting stone.

    Parameters
    ----------
    stone: str
        The number on the starting stone.

    Return
    ------
    List[str]
        The numbers of all the stones produced after the blink.
    """
    # If the stone is engraved with the number 0, then it's remplaced by a
    # stone engraved with the number 1.
    if stone == '0':
        return ['1']

    # If the stone is engraved with a number that has an even number of digit,
    # then it's remplaced by two stones:
    # - 1 stone with the left half of digit;
    # - 1 stone with the rich half of digit.
    if len(stone) % 2 == 0:
        mid = len(stone) // 2
        return [f"{int(stone[:mid]):d}", f"{int(stone[mid:]):d}"]

    # Otherwise the old stone's number is multiplied by 2024.
    return [f"{int(stone)*2024:d}"]


def blink(stones: List[str]) -> Dict[str, int]:
    """
    Computes all the stones produced after the blink of an eye.

    Parameters
    ----------
    stones: List[str]
        The list of stones present.

    Return
    ------
    Dict[str, int]
        A dictionary of the stones produced and their number after a blink.
    """
    result = {}
    for stone in stones:
        new_stones = change(stone)
        for new_stone in new_stones:
            if new_stone not in result:
                result[new_stone] = 0
            result[new_stone] += stones[stone]
    return result


if __name__ == "__main__":
    INPUT = sys.argv[1]

    t = time.time()

    with open(INPUT, "r", encoding="utf-8") as f:
        lines = f.readlines()
        stones = {stone: 1 for stone in re.findall("[0-9]+", lines[0])}

    FIRST = 0
    for i in range(0, 75):
        stones = blink(stones)
        # First part.
        if i == 24:
            FIRST = sum(n for n in stones.values())

    # Second part.
    SECOND = sum(n for n in stones.values())

    t = time.time() - t
    print(f"The first part result is {FIRST:d}.")
    print(f"The second part result is {SECOND:d}.")
    print(f"Found in {t:.5f}s!")
