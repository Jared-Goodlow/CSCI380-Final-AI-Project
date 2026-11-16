# Interactive Maze Solver Using AI Search Algorithms

**Course:** CSCI 380 - Artificial Intelligence  
**Team:** Jared Goodlow and Shiva Patel  
**Status:** Mid-progress Report

This project is a Python/Pygame application for comparing how BFS, DFS, and A* search through grid mazes. It uses **four-direction movement**, **unit movement costs**, and grid cells represented by `0` (open) and `1` (wall). The core search logic will be written in Python, not supplied by a maze-solving library.

## Requirements

- **Python 3.14 recommended** 
- **Pygame Community Edition** (`pygame-ce`), installed from `requirements.txt`.
- A desktop computer able to display a Pygame window. No external maze-solving package is required.

**Important:** The dependency is `pygame-ce`, but the code still correctly uses `import pygame`. Avoid installing the older `pygame` package in the same environment. Python 3.15 previously caused a build error with the original `pygame` package; the working configuration uses Python 3.14 and `pygame-ce`.

## Installation and setup

First, download or clone this repository. Open a terminal **in the folder containing `main.py` and `requirements.txt`**.

### Recommended: Windows (PowerShell) with a virtual environment

Run these three commands in order:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

- The first command creates a local `.venv` environment (only once).
- The second installs the dependency inside that environment (initial setup and whenever requirements change).
- The third starts the program (use this on subsequent runs).
- **No activation command is needed**: these commands explicitly use the environment's Python executable.

If `py -3.14` reports that the version is unavailable, install Python 3.14 or adjust the command to a compatible installed Python version. Check installed versions with `py -0p`.

### macOS / Linux

For a compatible Python 3 installation, the equivalent virtual-environment commands are:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Python and Pygame availability vary by operating system and Python version. The documented, confirmed working environment for this project is Windows with Python 3.14 and `pygame-ce`.

### VS Code interpreter selection (optional)

If VS Code underlines `import pygame` even though the application runs:

1. Open the Command Palette (`Ctrl+Shift+P`).
2. Select **Python: Select Interpreter**.
3. Choose your project's `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (macOS/Linux), if using a virtual environment.
4. Reopen the Python file or reload VS Code if necessary.

### Troubleshooting

- **`No module named 'pygame'`**: install dependencies with the **same Python executable** used to run `main.py`.
- **Pygame tries to compile from source or fails to build**: verify that `requirements.txt` contains `pygame-ce`, not the original `pygame` dependency; use a supported Python version. Our tested setup is Python 3.14 with `pygame-ce` 2.5.8.
- **The command exits without showing a window**: confirm that you have the full `main.py`, ending with `if __name__ == "__main__": main()`.
- **Git repository hygiene**: commit the `.py` files, `README.md`, `requirements.txt`, and `.gitignore`, but **do not commit `.venv/` or `__pycache__/`**. A `.gitignore` at the repository root should include at least `.venv/`, `__pycache__/`, and `*.pyc`.

## Controls

| Control | Action |
|---|---|
| Select **Walls**, then left-click/drag | Add walls, or click an existing wall to erase it |
| Select **Start** or **Goal**, then left-click | Move the relevant endpoint |
| Select **Erase** or right-click/drag | Remove walls |
| **1**, **2**, **3**, **4** | Load sample mazes (Starter, Detour, No Route, Start = Goal) |
| **B**, **D**, **A** | Choose BFS, DFS, or A* |
| **Space** or **Run Search** | Execute the selected algorithm |
| **R** or **Reset View** | Hide previous search results without changing the maze |
| **C** or **Clear Walls** | Remove all walls |
| **Esc** | Quit |

The interface colors represent walls, open cells, start, goal, expanded cells, and final route. Search time must measure **only the algorithm**, excluding animation.

## Project files

- `main.py` - Jared's graphical interface, maze editing, input checking, algorithm selection, and search-result animation.
- `mazes.py` - Jared's deterministic sample mazes and edge cases.
- `search.py` - Shared `SearchResult` interface and placeholder functions for Shiva's BFS, DFS, and A* implementations.
- `requirements.txt` - Pygame dependency.

## Current progress / remaining work

**Interface components present:** Pygame maze display; painting/removing walls; selecting/moving start and goal; loading four sample mazes; algorithm-selection controls; an animation engine for visited cells and routes; display of path length, expanded-cell count, and algorithm runtime when an algorithm returns results.

**BFS implementation:** BFS has been implemented and integrated with the application. It uses a queue to explore maze cells, reconstructs the shortest path when one exists, and records the number of expanded cells and execution time.

**Planned for final submission:** DFS, A*, further testing and performance comparisons, final report and presentation.

## Suggested manual tests before mid-progress submission

1. **Starter:** BFS should reach the goal through openings and display the full route.
2. **Detour:** BFS should reach the goal without crossing walls.
3. **No Route:** BFS should report no route and an empty `path`.
4. **Start = Goal:** BFS should return a single-cell path and zero moves.
5. **Edited maze:** Add and remove walls, reposition start/goal, then run BFS again.
6. **Reset:** Run BFS, choose Reset View, and confirm the maze stays unchanged.

## Group contributions

| Member | Actual completed work | Estimated contribution |
|---|---|---|
| Jared Goodlow | Pygame interface, maze editing controls, visualization, sample/test mazes | **60%** |
| Shiva Patel | BFS implementation, path reconstruction, testing | **40%** |
| **Total** | | **100%** |

