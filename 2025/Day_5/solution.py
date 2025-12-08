"""
Advent of code - Day 5 (2025)
"""
import re
import sys
import time


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    # Reads the input file and retrieves the food IDs and intervals that
    # indicate which ones are fresh.
    with open(INPUT, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        intervals = []
        foods = []
        for line in lines:
            if re.match(r"^\d+-\d+$", line):
                intervals.append([int(e) for e in line.split('-')])
            elif re.match(r"^\d+$", line):
                foods.append(int(line))

    # Sorts all intervals according to their first bound.
    intervals = sorted(intervals, key=lambda x: x[0])

    # Merge all intervals so that there are no overlapping intervals.
    i = 0
    merged = []
    while i < len(intervals):
        first = intervals[i]
        j = i + 1
        IS_MERGED = True
        # Merges all intervals that can be merged with the current one.
        while IS_MERGED and j < len(intervals):
            second = intervals[j]
            if first[1] >= second[0]:
                first = [
                    min(first[0], second[0]),
                    max(first[1], second[1])
                ]
                i += 1  # Increment to ignore the merged interval later.
                j += 1  # Increment to check if the next one can be merged.
            else:
                IS_MERGED = False

        # Appends the current element or the merge between several intervals.
        merged.append(first)
        i += 1

    # Count the number of fresh food items.
    FIRST = sum(
        1
        if any(start <= food <= end for start, end in merged)
        else 0
        for food in foods
    )
    # Counts the cumulative size of all intervals.
    SECOND = sum(
        end - start + 1
        for start, end in merged
    )

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
