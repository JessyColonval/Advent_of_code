"""
Advent of code - Day 12 (2024)
"""
import sys
import time


def extract_regions(garden):
    visited = [
        [False for j in range(0, len(garden[i]))]
        for i in range(0, len(garden))
    ]
    regions = []

    for i, line in enumerate(garden):
        for j, plant in enumerate(line):
            if not visited[i][j]:
                region = [(i, j)]
                visited[i][j] = True
                recursion(garden, plant, i, j, visited, region)
                regions.append(region)

    return regions


def recursion(garden, plant, i, j, visited, indices):
    # Above.
    ab = i-1
    if (ab >= 0 and garden[ab][j] == plant and not visited[ab][j]):
        visited[ab][j] = True
        indices.append((ab, j))
        recursion(garden, plant, ab, j, visited, indices)

    # Below.
    be = i+1
    if (be < len(garden) and garden[be][j] == plant and not visited[be][j]):
        visited[be][j] = True
        indices.append((be, j))
        recursion(garden, plant, be, j, visited, indices)

    # Right.
    ri = j+1
    if (ri < len(garden[i]) and garden[i][ri] == plant and not visited[i][ri]):
        visited[i][ri] = True
        indices.append((i, ri))
        recursion(garden, plant, i, ri, visited, indices)

    # Left.
    le = j-1
    if (le >= 0 and garden[i][le] == plant and not visited[i][le]):
        visited[i][le] = True
        indices.append((i, le))
        recursion(garden, plant, i, le, visited, indices)


def plant_perimeter(garden: list, i: int, j: int) -> int:
    plant = garden[i][j]
    result = 0

    # Check above the plant.
    if i-1 < 0 or garden[i-1][j] != plant:
        result += 1

    # Check below the plant.
    if i+1 >= len(garden) or garden[i+1][j] != plant:
        result += 1

    # Check at the right of the plant.
    if j+1 >= len(garden[i]) or garden[i][j+1] != plant:
        result += 1

    # Check at the left of the plant.
    if j-1 < 0 or garden[i][j-1] != plant:
        result += 1

    return result


def region_perimeter(garden, region):
    return sum(
        plant_perimeter(garden, coords[0], coords[1])
        for coords in region
    )


def divide_by_line(region):
    result = {}
    for plant in region:
        x = plant[0]
        if x not in result:
            result[x] = []
        result[x].append(plant)
    return {
        key: sorted(values, key=lambda t: t[1])
        for key, values in result.items()
    }


def divide_by_column(region):
    result = {}
    for plant in region:
        y = plant[1]
        if y not in result:
            result[y] = []
        result[y].append(plant)
    return {
        key: sorted(values, key=lambda t: t[0])
        for key, values in result.items()
    }


def count_sequence_of_true(sequence) -> int:
    count = 0
    in_sequence = False
    for e in sequence:
        if e:
            if not in_sequence:
                count += 1
                in_sequence = True
        else:
            in_sequence = False
    return count


def number_of_h_faces(garden, region_by_lines) -> int:
    N_LINES = len(garden)
    result = 0
    for line in region_by_lines.values():
        top = [False for _ in range(N_LINES)]
        bottom = [False for _ in range(N_LINES)]
        for x, y in line:
            if x-1 < 0 or garden[x-1][y] != garden[x][y]:
                top[y] = True
            if x+1 >= N_LINES or garden[x+1][y] != garden[x][y]:
                bottom[y] = True

        result += count_sequence_of_true(top)
        result += count_sequence_of_true(bottom)

    return result


def number_of_v_faces(garden, region_by_columns) -> int:
    N_COLUMNS = len(garden[0])
    result = 0
    for column in region_by_columns.values():
        left = [False for _ in range(0, N_COLUMNS)]
        right = [False for _ in range(0, N_COLUMNS)]
        for x, y in column:
            if y-1 < 0 or garden[x][y-1] != garden[x][y]:
                left[x] = True
            if y+1 >= N_COLUMNS or garden[x][y+1] != garden[x][y]:
                right[x] = True

        result += count_sequence_of_true(left)
        result += count_sequence_of_true(right)

    return result


def number_of_faces(garden, region) -> int:
    if (len(region) == 1
       or all(plant[0] == region[0][0] for plant in region)
       or all(plant[1] == garden[0][1] for plant in region)):
        return 4

    region_by_lines = divide_by_line(region)
    region_by_columns = divide_by_column(region)
    return number_of_h_faces(garden, region_by_lines) + \
        number_of_v_faces(garden, region_by_columns)


if __name__ == "__main__":
    INPUT = sys.argv[1]

    t = time.time()

    with open(INPUT, "r", encoding="utf-8") as f:
        garden = [
            [letter for letter in line if letter != '\n']
            for line in f.readlines()
        ]

    regions = extract_regions(garden)

    FIRST = 0
    SECOND = 0
    for plants in regions:
        # Computes the first part of this puzzle for the current region.
        perimeter = region_perimeter(garden, plants)
        FIRST += perimeter * len(plants)

        # Computes the second part of this puzzle for the current region.
        n_faces = number_of_faces(garden, plants)
        SECOND += n_faces * len(plants)

    t = time.time() - t

    print(f"The first part result is {FIRST:d}")
    print(f"The second part result is {SECOND:d}")
    print(f"Found in {t:0.5f}s!")
