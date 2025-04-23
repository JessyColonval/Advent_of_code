"""
Advent of code - Day 4
"""
import re
import sys
import time


if __name__ == "__main__":
    FILE_NAME = sys.argv[1]

    t = time.time()

    # Convert the contents of the file into a single string to apply our
    # regular expressions.
    # Line breaks are replaced by spaces, as .{INT} segments do not work with.
    DATA = ""
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = f.readlines()
        n = len(lines[0]) - 1
        for line in lines:
            DATA += line[:len(line)-1] + " "

    # Number of characters to skip to make a left or right diagonal.
    l = n + 1
    r = n - 1

    # First part.
    first = (
        len(re.findall("XMAS", DATA)) + len(re.findall("SAMX", DATA))
        + len(re.findall(f"(?=X.{{{n:d}}}M.{{{n:d}}}A.{{{n:d}}}S)", DATA))
        + len(re.findall(f"(?=S.{{{n:d}}}A.{{{n:d}}}M.{{{n:d}}}X)", DATA))
        + len(re.findall(f"(?=S.{{{l:d}}}A.{{{l:d}}}M.{{{l:d}}}X)", DATA))
        + len(re.findall(f"(?=X.{{{l:d}}}M.{{{l:d}}}A.{{{l:d}}}S)", DATA))
        + len(re.findall(f"(?=S.{{{r:d}}}A.{{{r:d}}}M.{{{r:d}}}X)", DATA))
        + len(re.findall(f"(?=X.{{{r:d}}}M.{{{r:d}}}A.{{{r:d}}}S)", DATA))
    )

    # Second part.
    second = (
        len(re.findall(f"(?=(M.{{1}}S.{{{r:d}}}A.{{{r:d}}}M.{{1}}S))", DATA))
        + len(re.findall(f"(?=(S.{{1}}M.{{{r:d}}}A.{{{r:d}}}S.{{1}}M))", DATA))
        + len(re.findall(f"(?=(S.{{1}}S.{{{r:d}}}A.{{{r:d}}}M.{{1}}M))", DATA))
        + len(re.findall(f"(?=(M.{{1}}M.{{{r:d}}}A.{{{r:d}}}S.{{1}}S))", DATA))
    )

    t = time.time() - t

    print(f"The first part result is: {first:d}.")
    print(f"The second part result is: {second:d}.")
    print(f"Found in {t:.5f}s!")
