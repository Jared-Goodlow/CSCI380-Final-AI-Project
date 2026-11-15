"""Deterministic maze examples and board dimensions for the Pygame interface.

Coordinates are (row, column). A 0 cell is traversable; a 1 cell is a wall.
This file intentionally contains no search-algorithm implementation.
"""

from __future__ import annotations

from dataclasses import dataclass

ROWS = 17
COLS = 25

Cell = tuple[int, int]
Grid = list[list[int]]


@dataclass
class MazePreset:
    name: str
    grid: Grid
    start: Cell
    goal: Cell


def _empty_board() -> Grid:
    grid = [[0] * COLS for _ in range(ROWS)]
    # Outer walls make it easy to see the edge of the maze.
    for col in range(COLS):
        grid[0][col] = 1
        grid[ROWS - 1][col] = 1
    for row in range(ROWS):
        grid[row][0] = 1
        grid[row][COLS - 1] = 1
    return grid


def _horizontal(grid: Grid, row: int, left: int, right: int, gaps: tuple[int, ...] = ()) -> None:
    for col in range(left, right + 1):
        if col not in gaps:
            grid[row][col] = 1


def _vertical(grid: Grid, col: int, top: int, bottom: int, gaps: tuple[int, ...] = ()) -> None:
    for row in range(top, bottom + 1):
        if row not in gaps:
            grid[row][col] = 1


def get_preset(index: int) -> MazePreset:
    """Return a *new* maze each call, so edits never modify the presets."""
    grid = _empty_board()
    start = (2, 2)
    goal = (14, 22)

    if index == 0:
        # Starter: several barriers with openings to route around.
        _horizontal(grid, 5, 1, 19, gaps=(7,))
        _horizontal(grid, 9, 5, 23, gaps=(17,))
        _horizontal(grid, 12, 1, 18, gaps=(4,))
        _vertical(grid, 12, 1, 4, gaps=(3,))
        _vertical(grid, 20, 10, 15, gaps=(14,))
        name = "Starter"
    elif index == 1:
        # Detour: zig-zag barriers that force longer routes.
        _vertical(grid, 6, 1, 13, gaps=(11,))
        _vertical(grid, 12, 3, 15, gaps=(5,))
        _vertical(grid, 18, 1, 13, gaps=(11,))
        _horizontal(grid, 7, 19, 23, gaps=(22,))
        name = "Detour"
    elif index == 2:
        # Unreachable: surround the goal on all four sides.
        _horizontal(grid, 6, 4, 19, gaps=(8, 15))
        for row, col in ((13, 22), (15, 22), (14, 21), (14, 23)):
            grid[row][col] = 1
        name = "No Route"
    elif index == 3:
        # Edge case: start and goal share a cell (zero moves).
        start = (8, 12)
        goal = start
        _horizontal(grid, 5, 3, 21, gaps=(12,))
        _horizontal(grid, 11, 3, 21, gaps=(12,))
        name = "Start = Goal"
    else:
        raise ValueError(f"Unknown maze preset index: {index}")

    # Endpoints must always be traversable.
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]] = 0
    return MazePreset(name, grid, start, goal)


PRESET_NAMES = ("Starter", "Detour", "No Route", "Start = Goal")
