"""
Advent of code - Day 12 (2024)
"""
from typing import List, Tuple, Dict

import sys
import time


def extract_regions(matrix: List[List[str]]) -> List[List[Tuple[int]]]:
    """
    Gives each different regions in the garden seperatly.

    Parameters
    ----------
    matrix : List[List[str]]
        Matrix that represents the garden.

    Result
    ------
    List[List[Tuple[int]]]
        A list for each different regions that contains the coordinates of
        plants presents in it.
    """
    # Matrix that indicates if a plant was already visited.
    visited = [
        [False for j in range(0, len(matrix[i]))]
        for i in range(0, len(matrix))
    ]

    result = []
    for i, line in enumerate(matrix):
        for j in range(len(line)):
            if not visited[i][j]:
                # If the current plant wasn't already visited then that means
                # this is a new area of plant.
                region = [(i, j)]

                # Set the current has visited.
                visited[i][j] = True

                # Find every adjacent similar plants until no new plant is
                # found.
                recursion(matrix, i, j, visited, region)

                # Append the region in the result.
                result.append(region)

    return result


def recursion(
        matrix: List[List[str]],
        i: int,
        j: int,
        visited: List[List[bool]],
        indices: List[Tuple[int]]
) -> None:
    """
    Find recursively every similar plant in one region, i.e. adjacent to at
    least one plant to the region.

    Parameters
    ----------
    matrix: List[List[str]]
        Matrix that represents the garden.
    i: int
        Coordinate x of the current plant.
    j: int
        Coordinate y of the currant plant.
    visited: List[List[bool]]
        Matrix of already visited plant in the garden.
    indices: List[Tuple[int]]
        A list of coordinates of similar plants in a region.
    """
    # Name of the current plant.
    plant = matrix[i][j]

    # Above.
    ab = i-1
    if (ab >= 0 and matrix[ab][j] == plant and not visited[ab][j]):
        visited[ab][j] = True
        indices.append((ab, j))
        recursion(matrix, ab, j, visited, indices)

    # Below.
    be = i+1
    if (be < len(matrix) and matrix[be][j] == plant and not visited[be][j]):
        visited[be][j] = True
        indices.append((be, j))
        recursion(matrix, be, j, visited, indices)

    # Right.
    ri = j+1
    if (ri < len(matrix[i]) and matrix[i][ri] == plant and not visited[i][ri]):
        visited[i][ri] = True
        indices.append((i, ri))
        recursion(matrix, i, ri, visited, indices)

    # Left.
    le = j-1
    if (le >= 0 and matrix[i][le] == plant and not visited[i][le]):
        visited[i][le] = True
        indices.append((i, le))
        recursion(matrix, i, le, visited, indices)


def plant_perimeter(matrix: List[List[str]], i: int, j: int) -> int:
    """
    Computes the perimeter of one plant.

    Parameters
    ----------
    matrix : List[List[str]]
        Matrix that represents the garden.
    i : int
        Coordinate x of the plant.
    j : int
        Coordinate y of the plant.

    Return
    ------
    int
        The perimeter of the plant at (i, j).
    """
    plant = matrix[i][j]  # Name of the plant at (i, j).
    n_lines = len(matrix)  # Number of lines
    n_cols = len(matrix[i])  # Number of columns.

    # Sets the result at zero.
    result = 0

    # Check above the plant.
    ab = i-1
    if ab < 0 or matrix[ab][j] != plant:
        result += 1

    # Check below the plant.
    be = i+1
    if be >= n_lines or matrix[be][j] != plant:
        result += 1

    # Check at the right of the plant.
    ri = j+1
    if ri >= n_cols or matrix[i][ri] != plant:
        result += 1

    # Check at the left of the plant.
    le = j-1
    if le < 0 or matrix[i][le] != plant:
        result += 1

    return result


def region_perimeter(matrix: List[List[str]],
                     indices: List[Tuple[int]]) -> int:
    """
    Computes the perimeter of a region.

    Parameters
    ----------
    matrix : List[List[str]]
        Matrix that represents the garden.
    indices: List[Tuple[int]]
        A list of coordinates of similar plants that shares the same region.

    Return
    ------
    int
        The perimeter of the given region.
    """
    return sum(
        plant_perimeter(matrix, x, y)
        for x, y in indices
    )


def divide_by_line(indices: List[Tuple[int]]) -> Dict[int, List[Tuple[int]]]:
    """
    Separates a region according to its lines.

    Parameters
    ----------
    indices : List[Tuple[int]]
        A list of coordinates of similar plants that shares the same region.

    Return
    ------
    Dict[int, List[Tuple[int]]]
        A dictionnary that map a number of line in the garden with the
        coordinates of every plant in the given region on this line.
    """
    result = {}
    for plant in indices:
        x = plant[0]
        if x not in result:
            result[x] = []
        result[x].append(plant)
    return {
        key: sorted(values, key=lambda t: t[1])
        for key, values in result.items()
    }


def divide_by_column(indices: List[Tuple[int]]) -> Dict[int, List[Tuple[int]]]:
    """
    Separates a region according to its columns.

    Parameters
    ----------
    indices : List[Tuple[int]]
        A list of coordinates of similar plants that shares the same region.

    Return
    ------
    Dict[int, List[Tuple[int]]]
        A dictionnary that map a number of column in the garden with the
        coordinates of every plant in the given region on this column.
    """
    result = {}
    for plant in indices:
        y = plant[1]
        if y not in result:
            result[y] = []
        result[y].append(plant)
    return {
        key: sorted(values, key=lambda t: t[0])
        for key, values in result.items()
    }


def count_sequence_of_true(sequence: List[bool]) -> int:
    """
    Count the number of sequence of 'True' in a given list.

    Parameters
    ----------
    sequence: List[bool]
        A list of bool.

    Return
    ------
    int
        The number of different sequence of 'True' in the given list.
    """
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


def number_of_h_faces(
    matrix: List[List[str]],
    region_by_lines: Dict[int, List[Tuple[int]]]
) -> int:
    """
    Computes the number of horizontal faces present for a given region.

    Parameters
    ----------
    matrix : List[List[str]]
        Matrix that represents the garden.
    region_by_lines : Dict[int, List[Tuple[int]]]
        Dictionary that links the coordinates of plants present in the region
        to each row number in the garden.

    Return
    ------
    int
        Number of horizontal faces.
    """
    n_lines = len(matrix)
    result = 0
    for line in region_by_lines.values():
        top = [False for _ in range(n_lines)]
        bottom = [False for _ in range(n_lines)]
        for x, y in line:
            if x-1 < 0 or matrix[x-1][y] != matrix[x][y]:
                top[y] = True
            if x+1 >= n_lines or matrix[x+1][y] != matrix[x][y]:
                bottom[y] = True

        result += count_sequence_of_true(top)
        result += count_sequence_of_true(bottom)

    return result


def number_of_v_faces(
    matrix: List[List[str]],
    region_by_cols: Dict[int, List[Tuple[int]]]
) -> int:
    """
    Computes the number of vertical faces present for a given region.

    Parameters
    ----------
    matrix : List[List[str]]
        Matrix that represents the garden.
    region_by_cols : Dict[int, List[Tuple[int]]]
        Dictionary that links the coordinates of plants present in the region
        to each column number in the garden.

    Return
    ------
    int
        Number of vertical faces.
    """
    n_cols = len(matrix[0])
    result = 0
    for column in region_by_cols.values():
        left = [False for _ in range(0, n_cols)]
        right = [False for _ in range(0, n_cols)]
        for x, y in column:
            if y-1 < 0 or matrix[x][y-1] != matrix[x][y]:
                left[x] = True
            if y+1 >= n_cols or matrix[x][y+1] != matrix[x][y]:
                right[x] = True

        result += count_sequence_of_true(left)
        result += count_sequence_of_true(right)

    return result


def number_of_faces(matrix: List[List[str]], indices: List[Tuple[int]]) -> int:
    """
    Parameters
    ----------
    matrix : List[List[str]]
        Matrix that represents the garden.
    indices : List[Tuple[int]]
        A list of coordinates of similar plants that shares the same region.

    Return
    ------
    int
        Number of faces.
    """
    if (len(indices) == 1
       or all(x == indices[0][0] for x, _ in indices)
       or all(y == indices[0][1] for _, y in indices)):
        return 4

    i_by_lines = divide_by_line(indices)
    i_by_columns = divide_by_column(indices)
    return number_of_h_faces(matrix, i_by_lines) + \
        number_of_v_faces(matrix, i_by_columns)


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
