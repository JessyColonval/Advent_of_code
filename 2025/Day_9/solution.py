"""
Advent of code - Day 8 (2025)
"""
from typing import List
import sys
import time


def rectangle_size(p: List[int], q: List[int]) -> int:
    """
    Calculates the size of a rectangle defined by two of its opposite corners.

    Parameters
    ----------
    p : List[int]
        One of its corners.
    q : List[int]
        A corner opposed to 'p'.

    Returns
    -------
    int
        The size of this rectangle.
    """
    return (abs(p[0] - q[0]) + 1) * (abs(p[1] - q[1]) + 1)


def is_point_in_segment(p: List[int], a: List[int], b: List[int]) -> bool:
    """
    Check if a point 'p' is on a segment [a;b].
    Parameters
    ----------
    p : List[int]
        Coordinates of the point that may on the segment.
    a : List[int]
        Coordinates of the first point of the segment.
    b : List[int]
        Coordinates of the second point of the segment.

    Returns
    -------
    bool
        True if the point is on the segment [a;b], false otherwise.
    """
    return (
        min(a[0], b[0]) <= p[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )


def shorten_segment(p0: List[int], p1: List[int]) -> List[List[int]]:
    """
    Reduces a segment defined by two points a and b so that it no longer
    contains a and b.
    Do nothing if the segment cannot be reduced, i.e. it contains only a and b.

    Parameters
    ----------
    p0 : List[int]
        Coordinates of the first segment point.
    p1 : List[int]
        Coordinates of the second segment point.

    Returns
    -------
    List[List[int]]
        The new segment after its reduction.
    """
    (x0, y0), (x1, y1) = p0, p1

    # Segment horizontal
    if y0 == y1:
        if abs(x1 - x0) <= 2:
            return [p0, p1]
        if x0 < x1:
            return [[x0+1, y0], [x1-1, y1]]
        return [[x0-1, y0], [x1+1, y1]]

    # Otherwise, the segment is vertical.
    if abs(y1 - y0) <= 2:
        return [p0, p1]
    if y0 < y1:
        return [[x0, y0 + 1], [x1, y1 - 1]]
    return [[x0, y0 - 1], [x1, y1 + 1]]


def segments_intersect(s0: List[List[int]], s1: List[List[int]]):
    """
    Check if two segments have an intersection.

    Parameters
    ----------
    s0 : List[List[int]]
        Coordinates of the two points of the first segment.
    s1 : List[List[int]]
        Coordinates of the two points of the second segment.

    Returns
    -------
        True if 's0' and 's1' have an intersection, false otherwise.
    """
    (x0, y0), (x1, y1) = s0
    (x2, y2), (x3, y3) = s1

    is_s1_h = y0 == y1
    is_s2_h = y2 == y3

    # First case: horizontal and vertical
    if is_s1_h != is_s2_h:
        # When s1 is horizontal and s2 is vertical.
        if is_s1_h:
            return (
                min(x0, x1) <= x2 <= max(x0, x1)
                and min(y2, y3) <= y0 <= max(y2, y3)
            )
        return (
            min(x2, x3) <= x0 <= max(x2, x3)
            and min(y0, y1) <= y2 <= max(y0, y1)
        )

    # Second case: both are horizontal.
    if is_s1_h:
        if y0 != y2:
            return False
        return max(x0, x1) >= min(x2, x3) and max(x2, x3) >= min(x0, x1)

    # Third case: both are vertical.
    if not is_s1_h:
        if x0 != x2:
            return False
        return max(y0, y1) >= min(y2, y3) and max(y2, y3) >= min(y0, y1)


def is_cut_by_an_edge(
    p: List[int],
    q: List[int],
    polygon_edges: List[List[List[int]]]
) -> bool:
    """
    Check if an edge of the rectangle is intersected by an edge of the main
    polygon.
    Note that the vertices of the rectangle must be on an edge of the main
    polygon, so they must be removed before calling this function.
    Moreover, an edge of the rectangle may overlap (completely or partially)
    an edge of the main polygon.

    Parameters
    ----------
    p : List[int]
        Coordinates of the first point of the segment.
    q : List[int]
        Coordinates of the second point of the segment.
    polygon_edges: List[List[List[in]
        All edges of the main polygon.

    Returns
    -------
    bool
        True if the edge of the rectangle is intersected by an edge of the
        given polygon, false otherwise.
    """
    # If the length of the rectangle's edge is 2, then this edge cannot be
    # crossed by an another edge of the main polygon.
    # Note that the edges are either vertical or horizontal.
    if abs(p[0] - q[0]) == 2 or abs(p[1] - q[1]) == 2:
        return False

    return any(
        not (
            is_point_in_segment(p, edge[0], edge[1])
            or is_point_in_segment(q, edge[0], edge[1])
            or is_point_in_segment(edge[0], p, q)
            or is_point_in_segment(edge[1], p, q)
        )
        and segments_intersect([p, q], edge)
        for edge in polygon_edges
    )


def has_right_edge(a: List[int], polygon_edges: List[List[List[int]]]) -> bool:
    """
    Check if one of the main polygon's edges is to the right of the given
    point, i.e., at the same x-coordinate.

    Parameters
    ----------
    a: List[int]
        Coordinates of the point.
    polygon_edges : List[List[List[int]]
        All edges of the main polygon.

    Returns
    -------
    bool
        True if a edge was found at the right of the given point.
    """
    for b, c in polygon_edges:
        x0 = min(b[0], c[0])
        if x0 >= a[0] and min(b[1], c[1]) <= a[1] <= max(b[1], c[1]):
            projection = [x0, a[1]]
            if is_point_in_segment(projection, b, c):
                return True
    return False


def has_left_edge(a: List[int], polygon_edges: List[List[List[int]]]) -> bool:
    """
    Check if one of the main polygon's edges is to the left of the given
    point, i.e., at the same x-coordinate.

    Parameters
    ----------
    a: List[int]
        Coordinates of the point.
    polygon_edges : List[List[List[int]]
        All edges of the main polygon.

    Returns
    -------
    bool
        True if a edge was found at the left of the given point.
    """
    for b, c in polygon_edges:
        x0 = min(b[0], c[0])
        if x0 <= a[0] and min(b[1], c[1]) <= a[1] <= max(b[1], c[1]):
            projection = [x0, a[1]]
            if is_point_in_segment(projection, b, c):
                return True
    return False


def has_bot_edge(a: List[int], polygon_edges: List[List[List[int]]]) -> bool:
    """
    Check if one of the main polygon's edges is to the bottom of the given
    point, i.e., at the same y-coordinate.

    Parameters
    ----------
    a: List[int]
        Coordinates of the point.
    polygon_edges : List[List[List[int]]
        All edges of the main polygon.

    Returns
    -------
    bool
        True if a edge was found at the bottom of the given point.
    """
    for b, c in polygon_edges:
        y0 = min(b[1], c[1])
        if y0 >= a[1] and min(b[0], c[0]) <= a[0] <= max(b[0], c[0]):
            projection = [a[0], y0]
            if is_point_in_segment(projection, b, c):
                return True
    return False


def has_top_edge(a: List[int], polygon_edges: List[List[List[int]]]) -> bool:
    """
    Check if one of the main polygon's edges is to the top of the given
    point, i.e., at the same y-coordinate.

    Parameters
    ----------
    a: List[int]
        Coordinates of the point.
    polygon_edges : List[List[List[int]]
        All edges of the main polygon.

    Returns
    -------
    bool
        True if a edge was found at the top of the given point.
    """
    for b, c in polygon_edges:
        y0 = min(b[1], c[1])
        if y0 <= a[1] and min(b[0], c[0]) <= a[0] <= max(b[0], c[0]):
            projection = [a[0], y0]
            if is_point_in_segment(projection, b, c):
                return True
    return False


def point_in_polygon(
    p: List[int],
    polygon_edges: List[List[List[int]]]
) -> bool:
    """
    Checks if a point is inside a polygon, i.e. if there is an edge in all 4
    directions of the point.

    Parameters
    ----------
    p : List[int]
        The coordinates point.
    polygon_edges : List[List[List[int]]]
        All edges of the main polygon.

    Returns
    -------
    bool
        True if the given point is in the given polygon, false otherwise.
    """
    return (
        has_bot_edge(p, polygon_edges)
        and has_top_edge(p, polygon_edges)
        and has_right_edge(p, polygon_edges)
        and has_left_edge(p, polygon_edges)
    )


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    # Reads the input file and retrieves the coordinates of the points and the
    # edges of the main polygon.
    with open(INPUT, 'r', encoding="utf-8") as f:
        points = [
            [int(val) for val in line.split(',')]
            for line in f.readlines()
        ]
        polygon = [
            [points[i], points[i+1]]
            for i in range(0, len(points)-1)
        ]
        polygon.append([points[-1], points[0]])

    # Associate the two indices of opposite points that form a rectangle with
    # its size.
    # Then sort in descending order by size.
    rectangles = {
        (i, j): rectangle_size(points[i], points[j])
        for i in range(0, len(points))
        for j in range(i+1, len(points))
    }
    rectangles = dict(
        sorted(rectangles.items(), key=lambda item: item[1], reverse=True)
    )

    # Gets the largest size.
    keys = list(rectangles.keys())
    FIRST = rectangles[keys[0]]

    SECOND = 0
    i = 0
    while SECOND == 0 and i < len(keys):
        rec_pts = keys[i]
        size = rectangles[rec_pts]

        # Four point of the rectangle
        r0 = points[rec_pts[0]]
        r2 = points[rec_pts[1]]
        r1 = [r2[0], r0[1]]
        r3 = [r0[0], r2[1]]

        if all(point_in_polygon(s, polygon)
               for s in (r1, r3)):
            edges = [
                shorten_segment(r0, r1),
                shorten_segment(r1, r2),
                shorten_segment(r2, r3),
                shorten_segment(r3, r0)
            ]
            if not any(is_cut_by_an_edge(A, B, polygon)
                       for A, B in edges):
                SECOND = size

        i += 1

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
