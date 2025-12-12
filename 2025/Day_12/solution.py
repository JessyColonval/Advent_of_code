"""
Advent of code - Day 12 (2025)
"""
import re
import sys
import time


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    with open(INPUT, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        regions = []
        patterns = []
        for line in lines:
            line = line.rstrip()
            # Creates a new empty pattern when the first line defining them is
            # encountered.
            if re.match(r"^\d+:$", line):
                patterns.append([])

            # Add a line to the last pattern that encodes the presence or
            # absence of a block using 0s and 1s.
            elif re.match(r"^[\.#]+$", line):
                patterns[-1].append([
                    1 if char == '#' else 0
                    for char in line
                ])

            # Adds a new region that is defined by its length, width, and a
            # list of indices of the patterns that must be found there.
            elif re.match(r"^\d+x\d+:(\s+\d+)+$", line):
                numbers = re.findall(r"\d+", line)
                regions.append([
                    int(numbers[0]),
                    int(numbers[1]),
                    [int(numbers[j]) for j in range(2, len(numbers))]
                ])

    FIRST = 0
    for length, width, gifts in regions:
        # Considers all required patterns as full.
        # Thus, if the region can already contain them, then there is no need
        # to search for a specific arrangement.
        max_size = sum(gifts) * 3
        if length >= max_size and width >= max_size:
            FIRST += 1
            continue

        # If the total number of blocks that make up the required patterns
        # exceeds the size of the region, then no arrangement can fit all the
        # patterns into the region.
        n_used_space = sum(
            n * sum(
                sum(line)
                for line in patterns[i]
            )
            for i, n in enumerate(gifts)
        )
        if n_used_space > (length * width):
            continue

        # ¯\_(ツ)_/¯
        FIRST += 1

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"Found in {t:0.5f}s!")
