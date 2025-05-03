"""
Advent of code - Day 8 (2024)
"""
import sys
import time
from collections.abc import Sequence, Mapping
from typing import Tuple, Set


def in_maps(maps: Sequence[Sequence[str]], coords: Sequence[int]) -> bool:
    """
    Checks if a 2D position is in the maps boundaries.

    Attributes
    ----------
    maps: Sequence[Sequence[str]]
        The maps where the position must be in.
    coords: Sequence[int]
        The coordinates of the position.

    Return
    ------
    bool
        true if the position is in the maps, false otherwise.
    """
    return (
        0 <= coords[0] < len(maps)
        and 0 <= coords[1] < len(maps[coords[0]])
    )


def symetric(first: Sequence[int], second: Sequence[int]) -> Tuple[int]:
    """
    Create the antinode of the second antenna according the first one.

    Attributes
    ----------
    first: Sequence[int]
        Coordinates of the first antenna.
    second: Sequence[int]
        Coordinates of the second antenna.

    Return
    ------
    Tuple[int]
        Coordinates of the antinode.
    """
    dx = second[0] - first[0]
    dy = second[1] - first[1]
    return (first[0]-dx, first[1]-dy)


def add_all_antinodes(first: Sequence[int], second: Sequence[int],
                      antinodes: Set[Tuple[int]],
                      maps: Sequence[Sequence[str]]) -> None:
    """
    Create all the antinodes of the second antenna according the first one that
    can be contains in the maps.

    Attributes
    ----------
    first: Sequence[int]
        Coordinates of the first antenna.
    second: Sequence[int]
        Coordinates of the second antenna.
    antinodes: Set[Tuple]
        A set that will contains the antinodes.
    maps: Sequence[Sequence[str]]
        A map where the antennas are and where the antinodes will be placed.
    """
    antinode = symetric(first, second)
    while in_maps(maps, antinode):
        antinodes.add(antinode)
        second = first
        first = antinode
        antinode = symetric(first, second)


def generate_antinodes(antennas: Mapping[str, Sequence[Tuple[int]]],
                       antinodes: Set[Tuple[int]],
                       maps: Sequence[Sequence[str]],
                       part: int = 1) -> None:
    """
    Add all the antinodes for all the antennas according to the conditions of
    the chosen part of the puzzle.

    Attributes
    ----------
    antennas: Mapping[str, Sequence[Tuple[int]]]
        A map containing the positions of all antennas for each frequency.
    antinodes: Set[Tuple[int]]
        A set that will contains the positions of all antinodes generated.
    maps: Sequence[Sequence[str]]
        A map where the antennas are and where the antinodes will be placed.
    part: int
        The number of the part of the puzzle that sets the conditions for
        adding antinodes.
    """
    if part == 1:
        for positions in antennas.values():
            for i0, p0 in enumerate(positions):
                for j0 in range(i0+1, len(positions)):
                    a0 = symetric(p0, positions[j0])
                    if in_maps(maps, a0):
                        antinodes.add(a0)
                    a1 = symetric(positions[j0], p0)
                    if in_maps(maps, a1):
                        antinodes.add(a1)

    elif part == 2:
        for positions in antennas.values():
            for i0, p0 in enumerate(positions):
                for j0 in range(i0+1, len(positions)):
                    add_all_antinodes(
                        p0, positions[j0],
                        antinodes, maps
                    )
                    add_all_antinodes(
                        positions[j0], p0,
                        antinodes, maps
                    )
                    antinodes.add(p0)
                    antinodes.add(positions[j0])

    else:
        raise ValueError("Unexpected part number!")


if __name__ == "__main__":
    t = time.time()
    file_name = sys.argv[1]

    MAPS = None
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
        MAPS = [
            [char for char in line if char != '\n']
            for line in lines
        ]

    antennas = {}
    for i, row in enumerate(MAPS):
        for j, element in enumerate(row):
            if element != '.':
                if element not in antennas:
                    antennas[element] = []
                antennas[MAPS[i][j]].append((i, j))

    # First part.
    antinodes = set()
    generate_antinodes(antennas, antinodes, MAPS)
    FIRST = len(antinodes)

    # Second part.
    antinodes = set()
    generate_antinodes(antennas, antinodes, MAPS, 2)
    SECOND = len(antinodes)

    t = time.time() - t

    # Prints the results.
    print(f"The first part result is {FIRST:d}.")
    print(f"The second part result is {SECOND:d}.")
    print(f"Found in {t:.5f}s!")
