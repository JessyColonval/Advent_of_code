"""
Advent of code - Day 8 (2025)
"""
from typing import List
import sys
import time
import heapq
from copy import deepcopy

import numpy as np


def get_index(value: int, lst: List[List[int]]) -> int | None:
    """
    Gets the index of the sublist that contains a given value.
    It is assumed that this value occurs only once.

    Parameters
    ----------
    value : int
        The value of the index to be searched.
    lst: List[List[int]]
        The main list containing all the lists that may contain the desired
        value.

    Returns
    -------
    int | None
        Index of the sub-list that contains the searched value or None if it is
        not present anywhere.
    """
    for i_lst, sublst in enumerate(lst):
        if value in sublst:
            return i_lst
    return None


if __name__ == "__main__":
    INPUT = sys.argv[1]
    LIMIT = int(sys.argv[2])  # Number of circuits for the first part.

    t = time.time()

    # Reads the input file and retrieves the coordinates of the boxes.
    with open(INPUT, 'r', encoding="utf-8") as f:
        boxes = np.array([
            [int(c) for c in line.split(',')]
            for line in f.readlines()
        ])

    # Euclidean distance matrix
    diff = boxes[:, None, :] - boxes[None, :, :]
    dist_matrix = np.sqrt(np.sum(diff**2, axis=2))

    # Keep the upper triangle of the matrix (i < j).
    i, j = np.triu_indices(len(boxes), k=1)
    distances = dist_matrix[i, j]

    # Sorting distances in ascending order.
    order = np.argsort(distances)

    # Created a list containing the index pairs of the closest boxes.
    sorted_pairs = list(zip(i[order], j[order]))

    circuits = []
    TMP_CIRCUITS = None
    IS_FIRST = False
    I_PAIR = 0
    while not IS_FIRST and I_PAIR < len(sorted_pairs):
        # Closest box indices.
        b0 = sorted_pairs[I_PAIR][0]
        b1 = sorted_pairs[I_PAIR][1]

        # Gets the indices of the circuits that contain the two current boxes.
        i_l0 = get_index(b0, circuits)
        i_l1 = get_index(b1, circuits)

        # If neither box is present in a link, then a new link is created.
        if i_l0 is None and i_l1 is None:
            circuits.append([b0, b1])

        # If the first box is not present in any link, but the second one is,
        # then the first one ends up in the same link as the second one.
        elif i_l0 is not None and i_l1 is None:
            circuits[i_l0].append(b1)

        # If the second box is not present in any link, but the first one is,
        # then the second one ends up in the same link as the first one.
        elif i_l0 is None and i_l1 is not None:
            circuits[i_l1].append(b0)

        # If the two boxes are present in two different circuits, then these
        # circuits are merged.
        elif i_l0 != i_l1:
            new_link = [*circuits[i_l0], *circuits[i_l1]]
            if i_l0 < i_l1:
                del circuits[i_l0], circuits[i_l1-1]
            else:
                del circuits[i_l1], circuits[i_l0-1]
            circuits.append(new_link)

        # Saves the link status at the LIMITth step.
        if I_PAIR == LIMIT-1:
            TMP_CIRCUITS = deepcopy(circuits)

        # Stop the loop when all the boxes are connected to each other.
        if (not IS_FIRST and len(circuits) == 1 and
           len(circuits[0]) == len(boxes)):
            IS_FIRST = True

        I_PAIR += 1

    # Gets the 3 largest circuit in the temporary circuit.
    largest = heapq.nlargest(3, TMP_CIRCUITS, key=len)

    FIRST = 1
    for circuit in largest:
        FIRST *= len(circuit)
    SECOND = boxes[b0][0] * boxes[b1][0]

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
