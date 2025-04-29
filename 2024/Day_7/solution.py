"""
Advent of code - Day 7 (2024)
"""
import re
import sys
import time
from collections.abc import Sequence


def convert_to_base3(n: int) -> str:
    """
    Converts a base-10 number into a base-3 number.

    Parameters
    ----------
    n: int
        An integer in base 10.

    Return
    ------
    str
        conversion of n to base 3.
    """
    if n == 0:
        return '0'
    base3_digits = []
    while n > 0:
        base3_digits.append(str(n % 3))
        n //= 3
    base3_digits.reverse()  # Reverse the list to get the correct order
    return ''.join(base3_digits)


def operation(left: int, right: int, operator: str) -> int:
    """
    Perform one of the three authorized operations.

    Attributes
    ----------
    left: int
        The left operand.
    right: int
        The right operand.
    operator: str
        The desired operation: 0 for +; 1 for * and 2 for ||.
        It is encoded with digits in character form to correspond to those
        present in binary or tertiary numbers without passing through an
        intermediate conversion.

    Return
    ------
    int
        the result of the operation choosen with the two values given.
    """
    if operator == '0':
        return right + left
    if operator == '1':
        return right * left
    if operator == "2":
        return int(f"{left:d}{right:d}")
    raise ValueError("Unknow operator!")


def is_equals(elements: Sequence[int], operators: str) -> bool:
    """
    Verifies that it is possible to obtain an expected result with a set of
    known values and operations.

    Attributes
    ----------
    elements: Sequence[int]
        A set of n integers containing the value expected at index 0 and the
        values that must produce it from index 1 to n-1.
    operators: str
        The list of operations to be performed in the order of the numbers
        encountered.
        It is encoded in the form of a binary and tertiary number.

    Return
    ------
        True if operations on numbers from 1 to n-1 result in the number
        with index 0, false otherwise.
    """
    n_operators = len(elements) - 2

    result = elements[1]
    expected = elements[0]

    # If the string encoding the operations to be performed is smaller than the
    # number of operator pairs, this means that the 1st operation (i.e. '+')
    # must be performed.
    # The result only increases, so if the result is higher than the expected
    # value, then the equation is inevitably wrong.
    i = len(operators)
    j = 2
    while result <= expected and i < n_operators:
        result += elements[j]
        i += 1
        j += 1

    i = 0
    while result <= expected and i < len(operators):
        result = operation(result, elements[j], operators[i])
        i += 1
        j += 1

    return result == expected


def is_correct(elements: Sequence[int], memory: Sequence[str],
               n_op: int) -> bool:
    """
    Verifies that it is possible to obtain an expected result for a set of
    known values with at least one combination of +, - and || operations.

    Attributes
    ----------
    elements: Sequence[int]
        A set of n integers containing the value expected at index 0 and the
        values that must produce it from index 1 to n-1.
    memory: Sequence[str]
        The set of possible +, *, || combinations encoded as a binary or
        tertiary number.
    n_op: int
        The n_op first combinations of operations in memory that can be made.

    Return
    ------
    bool
        True if there is at least one combination of operations to obtain the
        expected value with the values to be used, false otherwise.
    """
    return any(
        is_equals(elements, operators)
        for base10, operators in enumerate(memory)
        if base10 < n_op and operators is not None
    )


if __name__ == "__main__":
    FILE_NAME = sys.argv[1]

    t = time.time()

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = f.readlines()
        equations = [
            [int(value) for value in re.findall(r"[1-9][0-9]*", line)]
            for line in lines
        ]

    n_max_op = max(len(equation)-2 for equation in equations)

    ###########################################################################
    #                               First part.                               #
    ###########################################################################
    n_comb = 2**(n_max_op)
    base2 = [
        bin(value)[2:]
        for value in range(0, n_comb)
    ]

    # Store lines that can already be solved with the + and * operations, to
    # avoid having to calculate them again in part 2.
    FIRST = 0
    resolved = []
    for i_e, equation in enumerate(equations):
        if is_correct(equation, base2, 2**(len(equation)-2)):
            resolved.append(True)
            FIRST += equation[0]
        else:
            resolved.append(False)
    del base2
    ###########################################################################

    ###########################################################################
    #                              Second part.                               #
    ###########################################################################
    n_comb = 3**(n_max_op)
    base3 = []
    for value in range(0, n_comb):
        CONVERT = convert_to_base3(value)
        if '2' in CONVERT:
            base3.append(CONVERT)
        else:
            base3.append(None)
    SECOND = sum(
        equation[0]
        for i_e, equation in enumerate(equations)
        if resolved[i_e] or is_correct(equation, base3, 3**(len(equation)-2))
    )
    del base3
    ###########################################################################

    t = time.time() - t

    print(f"The first part result is {FIRST:d}.")
    print(f"The second part result is {SECOND:d}.")
    print(f"Found in {t:.5f}s!")
