"""Interactive Maze Solver — Pygame interface, editing, and animation.

Jared's portion: maze UI, mouse/keyboard tools, search-result display, sample
selection, and input validation. Search algorithms are supplied by search.py.

Run with: python main.py
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from mazes import COLS, ROWS, PRESET_NAMES, Cell, Grid, get_preset
from search import SearchResult, a_star, bfs, dfs

SCREEN_W, SCREEN_H = 1130, 805
CELL_SIZE = 27
GRID_X, GRID_Y = 28, 181
GRID_W, GRID_H = COLS * CELL_SIZE, ROWS * CELL_SIZE
SIDE_X, SIDE_Y, SIDE_W, SIDE_H = 735, 175, 365, 591
FPS = 60
STEP_INTERVAL = 0.018  # seconds per animated expanded-cell/path step

BG = (14, 21, 34)
PANEL = (25, 36, 55)
PANEL_HOVER = (40, 56, 78)
PANEL_ACTIVE = (48, 86, 127)
BORDER = (65, 84, 107)
WHITE = (236, 242, 251)
MUTED = (163, 183, 205)
OPEN = (227, 235, 243)
WALL = (73, 89, 111)
EXPLORED = (99, 174, 218)
ROUTE = (255, 197, 91)
START = (38, 185, 124)
GOAL = (228, 91, 99)
NOTICE = (255, 205, 122)
GOOD = (127, 230, 180)


@dataclass
class Button:
    rect: pygame.Rect
    label: str
    action: str
    value: str | int = ""


class MazeApp:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Interactive Maze Solver - CSCI 380")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("segoeui", 31, bold=True)
        self.h2_font = pygame.font.SysFont("segoeui", 20, bold=True)
        self.font = pygame.font.SysFont("segoeui", 16)
        self.small_font = pygame.font.SysFont("segoeui", 14)
        self.cell_font = pygame.font.SysFont("segoeui", 15, bold=True)
        self.tool = "Walls"
        self.algorithm = "BFS"
        self.drag_wall_value: int | None = None
        self.preset_index = 0
        self.grid: Grid = []
        self.start: Cell = (0, 0)
        self.goal: Cell = (0, 0)
        self.result: SearchResult | None = None
        self.reveal_visited = 0
        self.reveal_path = 0
        self.animating = False
        self.step_elapsed = 0.0
        self.status = ""
        self.status_color = MUTED
        self.buttons = self._make_buttons()
        self.load_preset(0)

    def _make_buttons(self) -> list[Button]:
        buttons: list[Button] = []
        for i, label in enumerate(("Walls", "Start", "Goal", "Erase")):
            buttons.append(Button(pygame.Rect(28 + i * 119, 113, 111, 43), label, "tool", label))
        for i, label in enumerate(("BFS", "DFS", "A*")):
            buttons.append(Button(pygame.Rect(754 + i * 110, 243, 99, 40), label, "algorithm", label))
        for i, label in enumerate(PRESET_NAMES):
            buttons.append(Button(pygame.Rect(754, 388 + i * 39, 326, 34), f"{i + 1}.  {label}", "preset", i))
        buttons.extend(
            (
                Button(pygame.Rect(754, 563, 158, 43), "Run Search", "run"),
                Button(pygame.Rect(922, 563, 158, 43), "Reset View", "reset"),
                Button(pygame.Rect(754, 615, 326, 37), "Clear Walls", "clear"),
            )
        )
        return buttons

    def set_status(self, message: str, color: tuple[int, int, int] = MUTED) -> None:
        self.status = message
        self.status_color = color

    def clear_search_display(self) -> None:
        self.result = None
        self.reveal_visited = 0
        self.reveal_path = 0
        self.animating = False
        self.step_elapsed = 0.0

    def load_preset(self, index: int) -> None:
        preset = get_preset(index)
        self.preset_index = index
        self.grid = preset.grid
        self.start = preset.start
        self.goal = preset.goal
        self.clear_search_display()
        self.set_status(f"Loaded {preset.name}. Choose an algorithm, or edit the maze.")

    def clear_walls(self) -> None:
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.clear_search_display()
        self.set_status("All walls removed. Start and goal cells were preserved.")

    def _cell_at(self, mouse_pos: tuple[int, int]) -> Cell | None:
        mx, my = mouse_pos
        col = (mx - GRID_X) // CELL_SIZE
        row = (my - GRID_Y) // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            return (row, col)
        return None

    def edit_cell(self, cell: Cell, mode: str, wall_value: int | None = None) -> None:
        row, col = cell
        if mode == "Walls":
            if cell == self.start or cell == self.goal:
                self.set_status("An endpoint cannot be turned into a wall.", NOTICE)
                return
            value = (1 - self.grid[row][col]) if wall_value is None else wall_value
            if self.grid[row][col] != value:
                self.grid[row][col] = value
                self.clear_search_display()
        elif mode == "Erase":
            if self.grid[row][col] == 1:
                self.grid[row][col] = 0
                self.clear_search_display()
        elif mode == "Start":
            if self.grid[row][col] == 1:
                self.grid[row][col] = 0
            self.start = cell
            self.clear_search_display()
            self.set_status(f"Start moved to row {row}, column {col}.")
        elif mode == "Goal":
            if self.grid[row][col] == 1:
                self.grid[row][col] = 0
            self.goal = cell
            self.clear_search_display()
            self.set_status(f"Goal moved to row {row}, column {col}.")

    def _on_mouse_down(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    self.activate(button)
                    return
            cell = self._cell_at(event.pos)
            if cell is None:
                return
            if self.tool in ("Walls", "Erase"):
                # Dragging applies the same operation instead of toggling cells repeatedly.
                self.drag_wall_value = (1 - self.grid[cell[0]][cell[1]]) if self.tool == "Walls" else 0
                self.edit_cell(cell, self.tool, self.drag_wall_value)
            else:
                self.edit_cell(cell, self.tool)
        elif event.button == 3:
            cell = self._cell_at(event.pos)
            if cell is not None:
                self.edit_cell(cell, "Erase")

    def _on_mouse_motion(self, event: pygame.event.Event) -> None:
        if event.buttons[0] and self.drag_wall_value is not None:
            cell = self._cell_at(event.pos)
            if cell is not None:
                self.edit_cell(cell, "Walls" if self.tool == "Walls" else "Erase", self.drag_wall_value)
        elif event.buttons[2]:
            cell = self._cell_at(event.pos)
            if cell is not None:
                self.edit_cell(cell, "Erase")

    def activate(self, button: Button) -> None:
        if button.action == "tool":
            self.tool = str(button.value)
            self.set_status(f"{self.tool} tool selected. Left-click cells on the grid.")
        elif button.action == "algorithm":
            self.algorithm = str(button.value)
            self.clear_search_display()
            self.set_status(f"Selected {self.algorithm}. Press Run Search to test it.")
        elif button.action == "preset":
            self.load_preset(int(button.value))
        elif button.action == "run":
            self.run_search()
        elif button.action == "reset":
            self.clear_search_display()
            self.set_status("Visualization cleared; maze layout is unchanged.")
        elif button.action == "clear":
            self.clear_walls()

    def _validate_result(self, result: SearchResult) -> None:
        """Catch integration mistakes before displaying misleading results."""
        if not isinstance(result, SearchResult):
            raise TypeError("Search function must return a SearchResult.")
        if not isinstance(result.elapsed_ms, (int, float)) or not (0 <= result.elapsed_ms < float("inf")):
            raise ValueError("elapsed_ms must be a nonnegative, finite number.")
        for cell in result.visited_order + result.path:
            if (
                not isinstance(cell, tuple) or len(cell) != 2
                or not all(isinstance(value, int) for value in cell)
            ):
                raise ValueError("Search cells must be (row, column) integer pairs.")
            row, col = cell
            if not (0 <= row < ROWS and 0 <= col < COLS) or self.grid[row][col] != 0:
                raise ValueError(f"Search returned a blocked or invalid cell: {cell}")
        if len(set(result.visited_order)) != len(result.visited_order):
            raise ValueError("visited_order must not repeat expanded cells.")
        if result.path:
            if result.path[0] != self.start or result.path[-1] != self.goal:
                raise ValueError("Returned path must begin at start and end at goal.")
            for first, second in zip(result.path, result.path[1:]):
                if abs(first[0] - second[0]) + abs(first[1] - second[1]) != 1:
                    raise ValueError("Every path move must go one cell up, down, left, or right.")

    def run_search(self) -> None:
        self.clear_search_display()
        if self.grid[self.start[0]][self.start[1]] or self.grid[self.goal[0]][self.goal[1]]:
            self.set_status("Invalid maze: start and goal must be open cells.", NOTICE)
            return
        search_functions = {"BFS": bfs, "DFS": dfs, "A*": a_star}
        try:
            # Give search a copy so it cannot accidentally modify the displayed maze.
            result = search_functions[self.algorithm](
                [row[:] for row in self.grid], self.start, self.goal
            )
            self._validate_result(result)
        except NotImplementedError as exc:
            self.set_status(str(exc), NOTICE)
            return
        except (TypeError, ValueError, IndexError) as exc:
            self.set_status(f"Search output error: {exc}", NOTICE)
            return

        self.result = result
        self.animating = bool(result.visited_order or result.path)
        if not result.path:
            self.set_status(f"{self.algorithm}: no route found. {result.expanded_count} cells expanded.", NOTICE)
        else:
            self.set_status(
                f"{self.algorithm}: found a route of {result.path_length} move(s). Animation playing.", GOOD
            )

    def _update_animation(self, dt: float) -> None:
        if not self.animating or self.result is None:
            return
        self.step_elapsed += dt
        while self.step_elapsed >= STEP_INTERVAL:
            self.step_elapsed -= STEP_INTERVAL
            if self.reveal_visited < len(self.result.visited_order):
                self.reveal_visited += 1
            elif self.reveal_path < len(self.result.path):
                self.reveal_path += 1
            else:
                self.animating = False
                if self.result.path:
                    self.set_status(
                        f"{self.algorithm}: completed. {self.result.path_length} moves, "
                        f"{self.result.expanded_count} expanded cells.", GOOD
                    )
                break

    def _text(self, content: str, x: int, y: int, color=WHITE, font=None) -> None:
        surface = (font or self.font).render(content, True, color)
        self.screen.blit(surface, (x, y))

    def _draw_button(self, button: Button, mouse_pos: tuple[int, int]) -> None:
        selected = (
            (button.action == "tool" and button.value == self.tool)
            or (button.action == "algorithm" and button.value == self.algorithm)
            or (button.action == "preset" and button.value == self.preset_index)
        )
        color = PANEL_ACTIVE if selected else PANEL_HOVER if button.rect.collidepoint(mouse_pos) else PANEL
        if button.action == "run":
            color = (44, 114, 114) if not button.rect.collidepoint(mouse_pos) else (54, 141, 140)
        pygame.draw.rect(self.screen, color, button.rect, border_radius=8)
        pygame.draw.rect(self.screen, BORDER if not selected else EXPLORED, button.rect, 1, border_radius=8)
        font = self.small_font if button.action == "preset" else self.font
        rendered = font.render(button.label, True, WHITE)
        self.screen.blit(rendered, rendered.get_rect(center=button.rect.center))

    def _draw_grid(self) -> None:
        outer = pygame.Rect(GRID_X - 5, GRID_Y - 5, GRID_W + 10, GRID_H + 10)
        pygame.draw.rect(self.screen, BORDER, outer, border_radius=5)
        visited = set(self.result.visited_order[:self.reveal_visited]) if self.result else set()
        path = set(self.result.path[:self.reveal_path]) if self.result else set()
        for row in range(ROWS):
            for col in range(COLS):
                cell = (row, col)
                color = WALL if self.grid[row][col] else OPEN
                if cell in visited:
                    color = EXPLORED
                if cell in path:
                    color = ROUTE
                if cell == self.start:
                    color = START
                if cell == self.goal:
                    color = GOAL
                rect = pygame.Rect(
                    GRID_X + col * CELL_SIZE,
                    GRID_Y + row * CELL_SIZE,
                    CELL_SIZE - 1,
                    CELL_SIZE - 1,
                )
                pygame.draw.rect(self.screen, color, rect, border_radius=2)
                if cell == self.start or cell == self.goal:
                    marker = "S/G" if self.start == self.goal else "S" if cell == self.start else "G"
                    text = self.cell_font.render(marker, True, WHITE)
                    self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_sidebar(self) -> None:
        pygame.draw.rect(self.screen, PANEL, pygame.Rect(SIDE_X, SIDE_Y, SIDE_W, SIDE_H), border_radius=12)
        self._text("SEARCH ALGORITHM", 754, 192, WHITE, self.h2_font)
        self._text("Implemented by the search.py module", 754, 220, MUTED, self.small_font)
        self._text("BFS is the mid-progress integration target.", 754, 297, MUTED, self.small_font)
        self._text("DFS and A* are planned for the final version.", 754, 317, MUTED, self.small_font)
        self._text("SAMPLE MAZES", 754, 353, WHITE, self.h2_font)
        self._text("RUN & RESET", 754, 529, WHITE, self.h2_font)
        self._text("SEARCH STATISTICS", 754, 666, WHITE, self.h2_font)
        if self.result is None:
            self._text("Moves: --    Expanded: --", 754, 697, MUTED, self.font)
            self._text("Algorithm time: -- ms", 754, 725, MUTED, self.font)
        else:
            move_count = str(self.result.path_length) if self.result.path else "No path"
            self._text(f"Moves: {move_count}    Expanded: {self.result.expanded_count}", 754, 697, WHITE, self.font)
            self._text(f"Algorithm time: {self.result.elapsed_ms:.3f} ms", 754, 725, WHITE, self.font)

    def _draw_bottom(self) -> None:
        self._text("STATUS", 28, 671, WHITE, self.h2_font)
        # Wrap status into at most two lines so an integration error is readable.
        words = self.status.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if self.font.size(candidate)[0] > GRID_W and current:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
        for i, line in enumerate(lines[:2]):
            self._text(line, 28, 702 + i * 21, self.status_color)
        self._text("Left-click: selected tool   |   Drag: paint/erase walls   |   Right-click: erase wall", 28, 755, MUTED, self.small_font)
        self._text("Keys: W/S/G/E = tools   1-4 = samples   B/D/A = algorithms   SPACE = run   R = reset   C = clear", 28, 778, MUTED, self.small_font)

    def draw(self) -> None:
        self.screen.fill(BG)
        self._text("INTERACTIVE MAZE SOLVER", 28, 20, WHITE, self.title_font)
        self._text("CSCI 380  /  Python + Pygame  /  Mid-progress project", 28, 66, MUTED, self.font)
        self._text("EDIT MAZE", 28, 87, WHITE, self.h2_font)
        self._text("Green = start     Red = goal     Blue = explored     Yellow = route", 526, 125, MUTED, self.small_font)
        self._draw_grid()
        self._draw_sidebar()
        self._draw_bottom()
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            self._draw_button(button, mouse_pos)
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._on_mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.drag_wall_value = None
                elif event.type == pygame.MOUSEMOTION:
                    self._on_mouse_motion(event)
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_ESCAPE:
                        running = False
                    elif key in (pygame.K_w, pygame.K_s, pygame.K_g, pygame.K_e):
                        self.tool = {
                            pygame.K_w: "Walls", pygame.K_s: "Start",
                            pygame.K_g: "Goal", pygame.K_e: "Erase",
                        }[key]
                        self.set_status(f"{self.tool} tool selected.")
                    elif key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                        self.load_preset(key - pygame.K_1)
                    elif key in (pygame.K_b, pygame.K_d, pygame.K_a):
                        self.algorithm = {pygame.K_b: "BFS", pygame.K_d: "DFS", pygame.K_a: "A*"}[key]
                        self.clear_search_display()
                        self.set_status(f"Selected {self.algorithm}.")
                    elif key == pygame.K_SPACE:
                        self.run_search()
                    elif key == pygame.K_r:
                        self.clear_search_display()
                        self.set_status("Visualization cleared; maze layout unchanged.")
                    elif key == pygame.K_c:
                        self.clear_walls()
            self._update_animation(dt)
            self.draw()
        pygame.quit()


def main() -> None:
    MazeApp().run()


if __name__ == "__main__":
    main()
