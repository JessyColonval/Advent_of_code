import os
import sys
import time
sys.path.append(os.path.abspath("../.."))

from reader import csv_to_list


if __name__ == '__main__':
    FILE_NAME = sys.argv[1]

    start = time.time()

    data = csv_to_list(FILE_NAME, "   ", "column")
    data[0].sort()
    data[1].sort()

    first = sum(
        abs(data[1][i] - data[0][i])
        for i in range(0, len(data[0]))
    )
    second = sum(
            e_left * sum(1 if e_right == e_left else 0 for e_right in data[1])
            for e_left in data[0]
    )

    end = time.time() - start

    print("First step solution: %d" % first)
    print("Second step solution: %d" % second)
    print("Found in %fs" % end)
