"""
Advent of code - Day 6 (2025)
"""
from typing import List
import sys
import time


def compute(first: int, second: int, operator: str) -> int:
    """
    Performs the + or * operation between two values.

    Parameters
    ----------
    first : int
        Value on the left.
    second : int
        Value on the right.
    operator : str
        The operation to be performed.

    Returns
    -------
    int
        The result of the operation.
    """
    match operator:
        case '+':
            return first + second
        case '*':
            return first * second
        case _:
            raise ValueError(f"Unexpected operator '{operator:}'!")


def resolve(values: List[int], operator: str) -> int:
    """
    Solves an equation consisting of a set of values and an operator.

    Parameters
    ----------
    values : List[int]
        The values of the equation in order.
    operator: str
        The operation to be applied to all values (+ or *).

    Returns
    -------
    int
        The result of the operations.
    """
    result = compute(values[0], values[1], operator)
    for i_val in range(2, len(values)):
        result = compute(result, values[i_val], operator)
    return result


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    with open(INPUT, 'r', encoding="utf-8") as f:
        lines = [
            line[:len(line)-1]  # Removes the last character that is '\n'.
            for line in f.readlines()
        ]

        # Get the operations and remove the line that encodes them to keep
        # only the values for the rest of the puzzle.
        operators = lines[-1].split()
        del lines[-1]

        # Get the values in the following reading direction: from left to right
        # and from top to bottom.
        N_EQUATIONS = len(lines[0].split())
        equations = [[] for _ in range(0, N_EQUATIONS)]
        for line in lines:
            for i, val in enumerate(line.split()):
                equations[i].append(int(val))

        # Get the values in the following reading direction: from bottom to
        # top.
        k = 0
        new_equations = [[] for _ in range(0, N_EQUATIONS)]
        for i in range(0, len(lines[0])):
            n = []
            for line in lines:
                if line[i] != ' ':
                    n.append(line[i])
            if len(n) > 0:
                new_equations[k].append(
                    int("".join(n))
                )
            else:
                k += 1

    # Performs operations with both reading directions.
    FIRST = sum(
        resolve(values, operators[i])
        for i, values in enumerate(equations)
    )
    SECOND = sum(
        resolve(values, operators[i])
        for i, values in enumerate(new_equations)
    )

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
