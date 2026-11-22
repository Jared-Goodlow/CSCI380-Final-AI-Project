# Interactive Maze Solver Using AI Search Algorithms

**Course:** CSCI 380 - Artificial Intelligence  
**Team:** Jared Goodlow and Shiva Patel  
**Status:** Core Application Implemented and Verified

This project is a Python/Pygame application for comparing how Breadth-First Search (BFS), Depth-First Search (DFS), and A* search through two-dimensional grid mazes. It uses **four-direction movement**, **unit movement costs**, and grid cells represented by `0` (open) and `1` (wall). Users can select a sample maze or edit the grid, place start and goal cells, choose a search algorithm, and watch the explored cells and final route appear on screen. The application also compares path length (moves), expanded-cell count, and algorithm execution time across the three methods on the same maze. The core search logic is written in Python, the graphical interface is supplied by Pygame, and this program does not use a maze-solving library. 

## Requirements

- **Python 3.14 recommended** 
- **Pygame Community Edition** (`pygame-ce`), installed from `requirements.txt`.
- No external maze-solving package is required.

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

If `py -3.14` reports that the version is unavailable, install Python 3.14 or adjust the command to a compatible installed Python version. 

### macOS / Linux

For a compatible Python 3 installation, the equivalent virtual-environment commands are:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python main.py
```

Python and Pygame availability vary by operating system and Python version. The documented and confirmed working environment for this project is Windows with Python 3.14 and `pygame-ce`.

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
| Select **Start** or **Goal**, then left-click | Move the relevant endpoint to an open cell (walls are rejected) |
| Select **Erase** or right-click/drag | Remove walls |
| **1**, **2**, **3**, **4** | Load sample mazes (Starter, Detour, No Route, Start = Goal) |
| **B**, **D**, **A** | Choose BFS, DFS, or A* |
| **Space** or **Run Search** | Execute the selected algorithm |
| **R** or **Reset View** | Clear the displayed route and exploration while keeping the maze and comparison results |
| **C** or **Clear Walls** | Remove all walls |
| **Esc** | Quit |

The interface colors represent walls, open cells, start, goal, expanded cells, and final route. Search time measures **only the algorithm**, excluding animation.

## Project files

- `main.py` - Jared's graphical interface, maze editing, input checking, algorithm selection, and search-result animation.
- `mazes.py` - Jared's deterministic sample mazes and edge cases.
- `search.py` - Shiva's implemented BFS, DFS, and A* algorithms and the shared `SearchResult` interface.
- `requirements.txt` - Pygame dependency.
- `.gitignore` - Excludes generated environments and Python cache files.
- `LICENSE` - Repository License (MIT)

## Current Progress

**Completed to Date:** The core maze-solving application has been implemented and the three search algorithms have been integrated into the Pygame interface. Jared completed the interactive grid, wall-editing and endpoint controls, four sample mazes, animated exploration and routes, input validation that rejects blocked endpoints, and a comparison display. Shiva completed BFS, DFS, and A*, including route reconstruction and measurement of expanded cells and execution time. Users can run each algorithm on the same maze, view its results, reset the visualization without changing the maze, and compare the algorithms' statistics. Changing the maze or endpoints clears outdated comparison results. 

**Implemented Search Algorithms:**
- **BFS:** Uses a queue to explore cells level by level and find a shortest route with equal movement costs.
- **DFS:** Uses a stack to explore a branch before backtracking; its route may be longer than the shortest route.
- **A*:** Uses a priority queue and Manhattan-distance heuristic to find a shortest route on the four-direction, equal-cost grid.

**Application Features:** Editable grid with start and goal placement, four preset mazes (Starter, Detour, No Route, Start = Goal), color-coded search animations, blocked-endpoint warnings, no-route handling, reset controls, and a comparison table showing moves, expanded cells, and algorithm execution time. Search timing excludes animation delays.

## Group contributions

| Member | Actual completed work | Estimated contribution |
|---|---|---|
| Jared Goodlow | Built the Pygame interface and editable grid; added wall and endpoint controls, blocked-endpoint validation, four test mazes, explored-cell and route animations, reset behavior, and the three-algorithm comparison display | **60%** |
| Shiva Patel | Implemented BFS, DFS, and A* using queues, stacks, and a priority queue with Manhattan distance; added path reconstruction, expanded-cell tracking, and execution-time statistics | **40%** |
| **Total** | | **100%** |

