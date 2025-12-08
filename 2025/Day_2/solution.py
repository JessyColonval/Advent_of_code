"""
Advent of code - Day 2 (2025)
"""
import re
import sys
import time


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    with open(INPUT, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        intervals = [
            [int(e) for e in interval.split('-')]
            for interval in lines[0].split(',')
        ]

    FIRST = 0
    SECOND = 0
    for start, end in intervals:
        for val in range(start, end+1):
            str_val = f"{val:d}"
            if re.match(r"^([0-9]+)\1+$", str_val):
                SECOND += val
                # There's no point in checking the pattern when the string is
                # an odd size, because it will always be wrong.
                if len(str_val) % 2 == 0 and re.match(r"^(.+)\1{1}$", str_val):
                    FIRST += val

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
