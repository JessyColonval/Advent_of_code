"""
Advent of code - Day 3
"""
import re
import sys
import time


if __name__ == '__main__':
    FILE_NAME = sys.argv[1]

    t = time.time()

    reg_int = "[1-9][0-9]*"
    reg_mul = f"mul\({reg_int:},{reg_int:}\)"
    reg_do = "do\(\)"
    reg_dont = "don't\(\)"
    reg = f"{reg_mul:}|{reg_do:}|{reg_dont:}"

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = f.readlines()

        # First part.
        first = 0
        for line in lines:
            matches = re.findall(reg_mul, line)
            for match in matches:
                m_val = re.findall(reg_int, match)
                first += int(m_val[0]) * int(m_val[1])

        # Second part.
        do = True
        second = 0
        for line in lines:
            matches = re.findall(reg, line)
            for match in matches:
                if match == "do()":
                    do = True
                elif match == "don't()":
                    do = False
                else:
                    if do:
                        m_val = re.findall(reg_int, match)
                        second += int(m_val[0]) * int(m_val[1])

    t = time.time() - t

    print(f"The first part result is: {first:d}.")
    print(f"The second part result is: {second:d}.")
    print(f"Found in {t:.5f}s!")
