from typing import Dict, List, Tuple
import numpy as np
import heapq as hq

from utils.read_input import read_input_as_matrix


def dijkstra(
    vertices: List[Tuple[int]],
    edges: Dict[Tuple[int], Dict[Tuple[int], int]],
    start: Tuple[int],
    destination: Tuple[int],
):
    visited = {v: False for v in vertices}
    distances = {v: float("inf") for v in vertices}
    paths = {v: None for v in vertices}
    queue = []
    distances[start] = 0
    hq.heappush(queue, (0, start))
    while queue:
        g, u = hq.heappop(queue)
        visited[u] = True
        if u == destination:
            return distances[destination]
        for v, w in edges[u].items():
            if not visited[v]:
                f = g + w
                if f < distances[v]:
                    distances[v] = f
                    paths[v] = u
                    hq.heappush(queue, (f, v))
    return paths, distances


if __name__ == "__main__":
    risk_map = np.array(read_input_as_matrix("day_15/input.txt", "int"))

    full_risk_map = np.vstack(
        [np.hstack([risk_map + i + j for j in range(5)]) for i in range(5)]
    )

    mask = full_risk_map > 9
    full_risk_map_mod = (full_risk_map % 10) + 1
    full_risk_map[mask] = full_risk_map_mod[mask]

    vertices = []
    edges = {}
    for i in range(len(full_risk_map)):
        for j in range(len(full_risk_map[i])):
            vertice = (i, j)
            vertices.append(vertice)
            neighbour_edges = {}
            for offset in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                neighbour = np.add(vertice, offset)
                if np.all(
                    np.logical_and(neighbour >= 0, neighbour < len(full_risk_map))
                ):
                    neighbour_edges[tuple(neighbour)] = full_risk_map[
                        neighbour[0], neighbour[1]
                    ]
            edges[vertice] = neighbour_edges

    start = (0, 0)
    destination = (len(full_risk_map) - 1, len(full_risk_map) - 1)
    print(dijkstra(vertices, edges, start, destination))
