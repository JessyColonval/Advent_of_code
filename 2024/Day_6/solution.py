"""
Advent of code - Day 6 (2024)
"""
import sys
import time
from Map import Map, Status

if __name__ == "__main__":
    FILE_NAME = sys.argv[1]

    t = time.time()

    _map = Map.build(FILE_NAME)
    x, y = _map.guard.coords

    # First part.
    _map.patrol()
    visited = _map.visited
    obstacles = set(
        (i, j)
        for i in range(0, len(visited))
        for j in range(0, len(visited[i]))
        if visited[i][j] and not (x == i and y == j)
    )
    FIRST = len(obstacles) + 1

    # Second part.
    SECOND = 0
    for xo, yo in obstacles:
        _map.add_temporary_obstacle(xo, yo)
        _map.patrol()
        if _map.status == Status.LOOP:
            SECOND += 1

    t = time.time() - t

    print(f"The first part result is: {FIRST:d}")
    print(f"The second part result is: {SECOND:d}")
    print(f"Found in {t:.5f}s!")
