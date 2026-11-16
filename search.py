"""Search algorithms for the maze solver (Shiva Patel).

main.py imports SearchResult and calls bfs/dfs/a_star. Each algorithm
works on a grid of 0 (open) and 1 (wall), moves up/down/left/right with
a cost of 1, and returns the cells it expanded, the route, and its runtime.
"""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass

Cell = tuple[int, int]  # (row, column)
Grid = list[list[int]]  # 0 means open, 1 means wall


@dataclass
class SearchResult:
    """Return one of these from each implemented search algorithm.

    visited_order: cells in expansion order; may include the start/goal.
    path: full route from start through goal (inclusive); [] if unreachable.
    elapsed_ms: algorithm runtime in milliseconds, excluding GUI animation.

    If start == goal, return path=[start] (0 moves), not an empty path.
    """

    visited_order: list[Cell]
    path: list[Cell]
    elapsed_ms: float

    @property
    def expanded_count(self) -> int:
        return len(self.visited_order)

    @property
    def path_length(self) -> int | None:
        return len(self.path) - 1 if self.path else None


def _neighbors(grid: Grid, cell: Cell):
    """Yield open cells one move away (up, down, left, right)."""
    row, col = cell
    for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        r, c = row + d_row, col + d_col
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == 0:
            yield (r, c)


def _reconstruct_path(parent: dict[Cell, Cell | None], goal: Cell) -> list[Cell]:
    """Follow parent links from the goal back to the start, then reverse."""
    path: list[Cell] = []
    cell: Cell | None = goal
    while cell is not None:
        path.append(cell)
        cell = parent[cell]
    path.reverse()
    return path


def bfs(grid: Grid, start: Cell, goal: Cell) -> SearchResult:
    """Breadth-First Search using a FIFO queue.

    Expands cells in order of distance from the start, so with equal move
    costs the first time it reaches the goal is along a shortest route.
    """
    t0 = time.perf_counter()

    frontier: deque[Cell] = deque([start])  # FIFO queue
    parent: dict[Cell, Cell | None] = {start: None}  # also acts as "seen" set
    visited_order: list[Cell] = []
    path: list[Cell] = []

    while frontier:
        cell = frontier.popleft()  # oldest cell first
        visited_order.append(cell)
        if cell == goal:
            path = _reconstruct_path(parent, goal)
            break
        for nxt in _neighbors(grid, cell):
            if nxt not in parent:  # never queue a cell twice
                parent[nxt] = cell
                frontier.append(nxt)

    elapsed_ms = (time.perf_counter() - t0) * 1000
    return SearchResult(visited_order, path, elapsed_ms)


def dfs(grid: Grid, start: Cell, goal: Cell) -> SearchResult:
    """Depth-First Search using a stack (final phase)."""
    raise NotImplementedError("DFS is planned for a later stage of the project.")


def a_star(grid: Grid, start: Cell, goal: Cell) -> SearchResult:
    """A* search with Manhattan distance (final phase)."""
    raise NotImplementedError("A* is planned for a later stage of the project.")