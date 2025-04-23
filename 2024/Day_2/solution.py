"""
Advent of code - Day 2
"""
import os
import sys
import time
from collections.abc import Sequence
sys.path.append(os.path.abspath("../.."))

from reader import csv_to_list


def is_all_increasing(report: Sequence[int]) -> bool:
    """Check if all element in a report is increasing"""
    return all(
            report[i_lvl] < report[i_lvl+1]
            for i_lvl in range(0, len(report)-1)
    )


def is_all_decreasing(report: Sequence[int]) -> bool:
    """Check if all element in a report is decreasing"""
    return all(
            report[i_lvl] > report[i_lvl+1]
            for i_lvl in range(0, len(report)-1)
    )


def is_good_diff(report: Sequence[int]) -> bool:
    """Check if the difference between all element is between 1 and 3."""
    return all(
            abs(report[i_lvl]-report[i_lvl+1]) >= 1
            and abs(report[i_lvl]-report[i_lvl+1]) <= 3
            for i_lvl in range(0, len(report)-1)
    )


def is_safe(report: Sequence[int]) -> int:
    """Check if a report is safe according to the conditions of part 1."""
    return (
        (is_all_increasing(report) or is_all_decreasing(report))
        and is_good_diff(report)
    )


def n_safe(reports: Sequence[Sequence[int]], part: int = 1) -> int:
    """
    Count the number of safe report according to the conditions of part 1 or 2.
    For the part 1, a report is safe when:
    - the levels are either all increasing or all decreasing;
    - and any two adjacent levels differ by at least one and at most three.
    For the part 2, a report is safe when:
    - is safe for the first part;
    - or is safe for the first part when only one level is removed.

    Parameters
    ----------
    reports: Sequence[Sequence[int]]
        all the report.
    part: int
        the number of the part that defines the conditions of a safe report.

    Returns
    -------
    int
        the number of safe report detected.

    Raises
    ------
    ValueError
        when part is different to 1 and 2.
    """
    if part == 1:
        return sum(
            1 if is_safe(report) else 0
            for report in reports
        )

    elif part == 2:
        count = 0
        for report in reports:
            if is_safe(report):
                count += 1
            else:
                i = 0
                is_found = False
                while i < len(report) and not is_found:
                    is_found = is_safe(report[:i] + report[i+1:])
                    i += 1
                if is_found:
                    count += 1
        return count

    else:
        raise ValueError("The part number must equal 1 or 2.")


if __name__ == '__main__':
    FILE_NAME = sys.argv[1]

    t = time.time()
    reports = csv_to_list(FILE_NAME, ' ')
    first = n_safe(reports, 1)
    second = n_safe(reports, 2)
    t = time.time() - t

    print(f"The first part result is: {first:d}")
    print(f"The second part result is: {second:d}")
    print(f"Found in {t:.5f}s !")
