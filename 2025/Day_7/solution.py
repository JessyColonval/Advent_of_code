"""
Advent of code - Day 7 (2025)
"""
import sys
import time


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    # Reads the input file and constructs the map where the tachyons will move.
    with open(INPUT, 'r', encoding="utf-8") as f:
        _map = [
            list(line.rstrip())
            for line in f.readlines()
        ]

    # A matrix representing the number of times a tachyon passes through each
    # cell.
    matrix = [
        [0 for _ in range(0, len(_map[i]))]
        for i in range(0, len(_map))
    ]

    FIRST = 0
    for i, line in enumerate(_map):
        for j, char in enumerate(line):
            # Tachyon starting point.
            if char == 'S':
                if i+1 < len(_map):
                    _map[i+1][j] = '|'
                    matrix[i+1][j] = 1

            # Tachyon beam.
            elif char == '|':
                if i+1 < len(_map):
                    # Tachyon separator.
                    if _map[i+1][j] == '^':
                        FIRST += 1  # Number of times a beam is split.

                        # If the map allows it, the beam is divided at the
                        # bottom right.
                        # Adds to the number of times the cell 'at the bottom
                        # right' has been visited by the one in the current
                        # cell.
                        if j-1 >= 0:
                            _map[i+1][j-1] = '|'
                            matrix[i+1][j-1] += matrix[i][j]

                        # If the map allows it, the beam is divided at the
                        # bottom left.
                        # Adds to the number of times the cell 'at the bottom
                        # left' has been visited by the one in the current
                        # cell.
                        if j+1 < len(_map[i+1]):
                            _map[i+1][j+1] = '|'
                            matrix[i+1][j+1] += matrix[i][j]

                    # Otherwise just extends the tachyon bean.
                    # Add to the number of times the cell 'below' has been
                    # visited by the one in the current cell.
                    elif _map[i+1][j] == '.' or _map[i+1][j] == '|':
                        _map[i+1][j] = '|'
                        matrix[i+1][j] += matrix[i][j]

    # The total number of different tachyon paths corresponds to the sum of
    # the number of visits to each cell in the last row.
    SECOND = sum(e for e in matrix[-1])

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
