import heapq
import time

from constants import wall


def neighbours(node, grid, rows, cols):
    r, c = node
    return [
        (r + dr, c + dc)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if 0 <= r + dr < rows and 0 <= c + dc < cols
        and grid[r + dr][c + dc] != wall
    ]


def build_path(came_from, end):
    path, node = [], end
    while node:
        path.append(node)
        node = came_from.get(node)
    return path[::-1]


def astar(grid, start, goal, h, rows, cols):
    t0 = time.perf_counter()
    pq = [(0, start)]
    came = {start: None}
    g = {start: 0}
    visited, frontier, closed = [], [], set()

    while pq:
        _, cur = heapq.heappop(pq)
        if cur in closed:
            continue
        closed.add(cur)
        visited.append(cur)

        if cur == goal:
            return {
                "found": True,
                "path": build_path(came, cur),
                "visited": visited,
                "frontier": frontier,
                "cost": g[cur],
                "time": round((time.perf_counter() - t0) * 1000, 2),
            }

        for nb in neighbours(cur, grid, rows, cols):
            new_g = g[cur] + 1
            if new_g < g.get(nb, float("inf")):
                came[nb] = cur
                g[nb] = new_g
                heapq.heappush(pq, (new_g + h(nb, goal), nb))
                frontier.append(nb)

    return {
        "found": False, "path": [], "visited": visited,
        "frontier": frontier, "cost": 0,
        "time": round((time.perf_counter() - t0) * 1000, 2),
    }


def gbfs(grid, start, goal, h, rows, cols):
    t0 = time.perf_counter()
    pq = [(h(start, goal), start)]
    came = {start: None}
    seen = {start}
    visited, frontier = [], []

    while pq:
        _, cur = heapq.heappop(pq)
        visited.append(cur)

        if cur == goal:
            path = build_path(came, cur)
            return {
                "found": True,
                "path": path,
                "visited": visited,
                "frontier": frontier,
                "cost": len(path) - 1,
                "time": round((time.perf_counter() - t0) * 1000, 2),
            }

        for nb in neighbours(cur, grid, rows, cols):
            if nb not in seen:
                seen.add(nb)
                came[nb] = cur
                heapq.heappush(pq, (h(nb, goal), nb))
                frontier.append(nb)

    return {
        "found": False, "path": [], "visited": visited,
        "frontier": frontier, "cost": 0,
        "time": round((time.perf_counter() - t0) * 1000, 2),
    }
