"""
Advent of code - Day 1 (2025)
"""
import sys
import time


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    # Reads the entry and organizes the data in the following format:
    # [ (DIRECTION, DISTANCE), ... ]
    with open(INPUT, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        document = [
            (line[0], int(line[1:]))
            for line in lines
        ]

    FIRST = 0
    SECOND = 0
    ARROW = 50
    for direction, distance in document:
        if direction == 'R':
            rotation = (ARROW + distance) // 100
            ARROW = (ARROW + distance) % 100

        elif direction == 'L':
            # Place the arrow in the positives values to calculate rotation in
            # the same way as 'R'.
            rotation = (((100 - ARROW) % 100) + distance) // 100
            ARROW = (ARROW - distance) % 100

        else:
            raise ValueError("Unexpected direction!")

        # First part solution count the number of times the arrow points at 0.
        # Second part solution count the number of times the arrow passes at 0.
        SECOND += rotation
        if ARROW == 0:
            FIRST += 1

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}!")
    print(f"The second part solution is {SECOND:d}!")
    print(f"Found in {t:0.5f}s!")
