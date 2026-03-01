import random

from constants import empty, wall


def make_grid(rows, cols):
    return [[empty] * cols for _ in range(rows)]


def generate_maze(rows, cols, density, start, goal):
    grid = [
        [wall if random.random() < density else empty for _ in range(cols)]
        for _ in range(rows)
    ]
    grid[start[0]][start[1]] = empty
    grid[goal[0]][goal[1]] = empty
    return grid
