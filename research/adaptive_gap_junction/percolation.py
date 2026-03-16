from __future__ import annotations


def has_spanning_cluster(lattice_size: int, occupied_edges: dict[tuple[int, int], float], active_nodes: set[int]) -> bool:
    adjacency: dict[int, set[int]] = {node: set() for node in active_nodes}
    for (i, j), scale in occupied_edges.items():
        if scale <= 0.0 or i not in active_nodes or j not in active_nodes:
            continue
        adjacency.setdefault(i, set()).add(j)
        adjacency.setdefault(j, set()).add(i)

    visited: set[int] = set()
    for start in list(adjacency):
        if start in visited:
            continue
        stack = [start]
        touches_left = False
        touches_right = False
        touches_top = False
        touches_bottom = False
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            row, col = divmod(node, lattice_size)
            touches_top = touches_top or row == 0
            touches_bottom = touches_bottom or row == lattice_size - 1
            touches_left = touches_left or col == 0
            touches_right = touches_right or col == lattice_size - 1
            for other in adjacency.get(node, ()):
                if other not in visited:
                    stack.append(other)
        if (touches_left and touches_right) or (touches_top and touches_bottom):
            return True
    return False
