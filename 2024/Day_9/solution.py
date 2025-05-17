"""
Advent of code - Day 9 (2024)
"""
import sys
import time
from Disk import Disk


if __name__ == "__main__":
    t = time.time()
    INPUT = sys.argv[1]

    DISK1 = None
    with open(INPUT, "r", encoding="utf-8") as f:
        lines = f.readlines()
        DISK2 = Disk.build_from_string(lines[0][:len(lines[0])-1])

        DISK1 = []
        FID = 0
        for i, char in enumerate(lines[0]):
            if char != '\n':
                val = int(char)
                if i % 2 == 0:
                    for j in range(0, val):
                        DISK1.append(FID)
                    FID += 1
                else:
                    for j in range(0, val):
                        DISK1.append(-1)

    if DISK1 is None or DISK2 is None:
        raise ValueError("The input wasn't parse.")

    # First part.
    i = 0
    j = len(DISK1)-1
    while i < j:
        if DISK1[i] == -1:
            if DISK1[j] == -1:
                j -= 1
            else:
                tmp = DISK1[i]
                DISK1[i] = DISK1[j]
                DISK1[j] = tmp
        else:
            i += 1

    FIRST = sum(
        i * DISK1[i] if DISK1[i] != -1 else 0
        for i in range(0, len(DISK1))
    )

    # Second part.
    DISK2.fragmentation()
    SECOND = DISK2.score()

    t = time.time() - t

    print(f"The first part result is {FIRST:d}.")
    print(f"The second part result is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
