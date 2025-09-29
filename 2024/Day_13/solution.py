"""
Advent of code - Day 13 (2024)
"""
from typing import List

import re
import sys
import time


def get_numbers(msg: str) -> List[int]:
    """
    Retrieves the numbers present in a string.

    Parameters
    ----------
    msg : str
        The string containing the numbers to be retrieved.

    Return
    ------
    List[int]
        All numbers found in the string.
    """
    return [
        int(str_nb)
        for str_nb in re.findall(r"[1-9][0-9]*", msg)
    ]


def n_button_a(a: int, b: int, c: int, d: int, e: int, f: int) -> float:
    """
    Calculates the minimum number of times the A button must be pressed to
    get the price.
    This number can be calculated from the x and y movements of buttons A and
    B and the coordinates of the price, using the following equation:
        Ax + By = C and Dx + Ey = F
        <=> E(Ax + By) = CE and B(Dx + Ey) = BF
        <=> E(Ax + By) - B(Dx + Ey) = CE - BF
        <=> EAx + EBy - BDx - BEy = CE - BF
        <=> EAx - BDx = CE - BF
        <=> x(EA - BD) = CE - BF
        <=> x = (CE - BF) / (EA - BD)

    Parameters
    ----------
    a : int
        The x-movement of the clamp when button A is pressed.
    b : int
        The y-movement of the clamp when button A is pressed.
    c : int
        The x-position of the price.
    d : int
        The x-movement of the clamp when button B is pressed.
    e : int
        The y-movement of the clamp when button B is pressed.
    f : int
        The y-position of the price.

    Return
    ------
    float
        The minimum number of times you must press the A button.
    """
    return (c*e-b*f)/(e*a-b*d)


def n_button_b(a: int, b: int, c: int, d: int, e: int, f: int) -> float:
    """
    Calculates the minimum number of times the B button must be pressed to
    get the price.
    This number can be calculated from the x and y movements of buttons A and
    B and the coordinates of the price, using the following equation:
        Ax + By = C and Dx + Ey = F
        <=> D(Ax + By) = DC and A(Dx + Ey) = AF
        <=> D(Ax + By) - A(Dx + Ey) = DC - AF
        <=> DAx + DBy - ADx - AEy = DC - AF
        <=> DBy - AEy = DC - AF
        <=> y(DB - AE) = DC - AF
        <=> y = (DC - AF) / (DB - AE)

    Parameters
    ----------
    a : int
        The x-movement of the clamp when button A is pressed.
    b : int
        The y-movement of the clamp when button A is pressed.
    c : int
        The x-position of the price.
    d : int
        The x-movement of the clamp when button B is pressed.
    e : int
        The y-movement of the clamp when button B is pressed.
    f : int
        The y-position of the price.

    Return
    ------
    float
        The minimum number of times you must press the B button.
    """
    return (d*c-a*f)/(d*b-a*e)


if __name__ == "__main__":
    INPUT = sys.argv[1]

    t = time.time()

    with open(INPUT, 'r', encoding="utf-8") as f:
        BUTTONS_A = []
        BUTTONS_B = []
        PRIZES = []
        for line in f.readlines():
            claw = {}
            if re.match(r"^Button A:", line):
                nbs = get_numbers(line)
                BUTTONS_A.append((nbs[0], nbs[1]))
            elif re.match(r"^Button B:", line):
                nbs = get_numbers(line)
                BUTTONS_B.append((nbs[0], nbs[1]))
            elif re.match(r"^Prize:", line):
                nbs = get_numbers(line)
                PRIZES.append((nbs[0], nbs[1]))

    FIRST = 0
    SECOND = 0
    for i, b_a in enumerate(BUTTONS_A):
        # Initializes equation's variables.
        a = b_a[0]
        b = BUTTONS_B[i][0]
        c = PRIZES[i][0]
        d = b_a[1]
        e = BUTTONS_B[i][1]
        f = PRIZES[i][1]

        # Computes the first part result.
        x = n_button_a(a, b, c, d, e, f)
        y = n_button_b(a, b, c, d, e, f)
        if x.is_integer() and y.is_integer():
            FIRST += (int(x)*3 + int(y))

        # Computes the second part result.
        c = c + 10000000000000
        f = f + 10000000000000
        x = n_button_a(a, b, c, d, e, f)
        y = n_button_b(a, b, c, d, e, f)
        if x.is_integer() and y.is_integer():
            SECOND += (int(x)*3 + int(y))

    t = time.time() - t

    print(f"The first part result is {FIRST:d}")
    print(f"The second part result is {SECOND:d}")
    print(f"Found in {t:0.5f}s!")
