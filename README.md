# Pathfinding Agent

A visual pathfinding simulator built with Python and Tkinter. Watch A\* and Greedy Best-First Search navigate a grid in real time, with support for dynamic obstacles and live replanning.

---

## Requirements

- Python 3.8+
- Tkinter (included with most Python installations)

---

## Running

```bash
python main.py
```

---

## File Structure

```
pathfinding_agent/
├── main.py          # Entry point
├── app.py           # Main controller
├── constants.py     # Cell types and colors
├── heuristics.py    # Manhattan and Euclidean distance
├── algorithms.py    # A* and Greedy BFS
├── grid.py          # Grid creation and maze generation
├── panel.py         # Left sidebar UI
└── canvas.py        # Grid rendering and mouse input
```

---

## Features

- **Algorithms** — A\* Search and Greedy Best-First Search
- **Heuristics** — Manhattan and Euclidean distance
- **Map Editor** — Draw/erase walls, reposition start and goal
- **Maze Generator** — Random obstacle generation with adjustable density
- **Animation** — Step-by-step visualization of visited nodes, frontier, and final path
- **Dynamic Mode** — Agent traverses the path while random obstacles spawn; replans automatically if the path is blocked
- **Metrics** — Displays nodes visited, path cost, and search time

---

## How to Use

1. **Set up the grid** — Use the map editor to draw walls, or click **generate** for a random maze.
2. **Choose an algorithm and heuristic** from the left panel.
3. Click **▶ run search** to start the visualization.
4. Enable **dynamic obstacles** to watch the agent move and replan in real time.
5. Click **⏹ stop** at any time to halt the animation.
