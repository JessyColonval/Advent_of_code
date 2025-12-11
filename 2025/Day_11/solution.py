"""
Advent of code - Day 8 (2025)
"""
from typing import Dict, List
import sys
import time
from copy import deepcopy
from collections import deque


def dfs(graph: Dict[str, List[str]], start: str, destination: str) -> int:
    """
    Perform an iterative DFS and count the number of paths that exist between a
    starting node and an end one.

    Parameters
    ----------
    graph : Dict[str, List[str]]
        A dictionary encoding the graph such that each value are nodes
        accessible from the key node.
    start : str
        The starting node.
    end : str
        The ending node.

    Returns
    -------
    int
        The number of path between 'start' and 'end'.
    """
    result = 0

    # Initializes a dictionary of nodes to indicate which ones have been
    # visited.
    visited = {}
    for parent, childs in graph.items():
        visited[parent] = False
        for child in childs:
            visited[child] = False

    # Mark the starting node as visited.
    visited[start] = True

    # Initializes the stack that contains the nodes encountered and those he
    # visited before.
    stack = deque()
    stack.append(
        (start, visited)
    )

    while len(stack) > 0:
        # Gets the current node and its visited nodes.
        node, visited = stack.pop()

        if node in graph:
            # Iterates its neigbors.
            for neighbor in graph[node]:
                # Increments the result if the current neighbor is the
                # destination.
                if neighbor == destination:
                    result += 1

                # Otherwise, if the current node is not already visited then
                # mark it as visited and add to the stack the neighbors and its
                # visited nodes.
                elif not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(
                        (neighbor, deepcopy(visited))
                    )

    return result


def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """
    Sort a graph in topological order, i.e., each node should not be accessible
    by the following nodes in the list.

    Parameters
    ----------
    graph : Dict[str, List[str]]
        A dictionary encoding the graph such that each value are nodes
        accessible from the key node.

    Returns
    -------
    List[str]
        Nodes in topological order.
    """
    # Initializes a dictionary of nodes to indicate which ones have been
    # visited.
    visited = {}
    for parent, childs in graph.items():
        visited[parent] = False
        for child in childs:
            visited[child] = False

    # Initializes the list of nodes in topological order.
    topo = [None for _ in visited]
    i = len(topo) - 1

    for start in graph:
        # No need to process the root if it has already been visited.
        # That means that all these children were too.
        if visited[start]:
            continue

        # Adds the root to the stack and marks it as visited once (status at
        # 0).
        stack = [(start, 0)]

        while len(stack) > 0:
            node, state = stack.pop()

            # Adds the node to the result if it status is 1.
            if state == 1:
                topo[i] = node
                i -= 1
                continue

            # No need to process the node if it has already been visited.
            if visited[node]:
                continue

            # Mark the current node as visited mark it as visited twice (status
            # to 1).
            visited[node] = True
            stack.append((node, 1))

            # Adds all its neighbors to the stack and marks them as visited
            # once (status at 0).
            if node in graph:
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append((neighbor, 0))

    return topo


def count_paths(graph: Dict[str, List[str]], topo: List[str], start: str,
                end: str) -> int:
    """
    Count the number of paths that exist between the starting point and the
    destination.

    Parameters
    ----------
    graph : Dict[str, List[str]]
        A dictionary encoding the graph such that each value are nodes
        accessible from the key node.
    topo : List[str]
        Nodes of the given graph in a topological order.
    start : str
        The starting node.
    end : str
        The ending node.

    Returns
    -------
    int
        The number of path between 'start' and 'end'.
    """
    ways = {node: 0 for node in topo}
    ways[start] = 1

    for u in topo:
        if u in graph:
            for v in graph[u]:
                ways[v] += ways[u]

    return ways[end]


if __name__ == "__main__":
    INPUT = sys.argv[1]
    t = time.time()

    with open(INPUT, 'r', encoding="utf-8") as f:
        given_graph = {
            line[0:3]: line[5:].rstrip().split(' ')
            for line in f.readlines()
        }

    sorted_graph = topological_sort(given_graph)
    FIRST = count_paths(given_graph, sorted_graph, "you", "out")

    SVR_DAC = count_paths(given_graph, sorted_graph, "svr", "dac")
    DAC_FFT = count_paths(given_graph, sorted_graph, "dac", "fft")
    FFT_OUT = count_paths(given_graph, sorted_graph, "fft", "out")
    SVR_FFT = count_paths(given_graph, sorted_graph, "svr", "fft")
    FFT_DAC = count_paths(given_graph, sorted_graph, "fft", "dac")
    DAC_OUT = count_paths(given_graph, sorted_graph, "dac", "out")
    SECOND = (
        (SVR_DAC * DAC_FFT * FFT_OUT)
        +
        (SVR_FFT * FFT_DAC * DAC_OUT)
    )

    t = time.time() - t

    print(f"The first part solution is {FIRST:d}.")
    print(f"The second part solution is {SECOND:d}.")
    print(f"Found in {t:0.5f}s!")
