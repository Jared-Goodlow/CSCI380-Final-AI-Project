"""Shared search interface — algorithm bodies belong to Shiva's portion.

The Pygame UI in main.py imports SearchResult and calls bfs/dfs/a_star.
Shiva -> replace the NotImplementedError statements with actual algorithms.
Do NOT invent a path or return hard-coded visited cells: the mid-progress
submission must demonstrate a genuine AI search technique.
"""

from __future__ import annotations

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


def bfs(grid: Grid, start: Cell, goal: Cell) -> SearchResult:
    """Shiva: implement Breadth-First Search here using a FIFO queue."""
    raise NotImplementedError("BFS is not yet implemented. Shiva will add it in search.py.")


def dfs(grid: Grid, start: Cell, goal: Cell) -> SearchResult:
    """Shiva: implement Depth-First Search here using a stack (final phase)."""
    raise NotImplementedError("DFS is planned for a later stage of the project.")


def a_star(grid: Grid, start: Cell, goal: Cell) -> SearchResult:
    """Shiva: implement A* with Manhattan distance (final phase)."""
    raise NotImplementedError("A* is planned for a later stage of the project.")
