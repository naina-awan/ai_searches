import tkinter as tk
import threading
import random

from constants import empty, wall
from heuristics import manhattan, euclidean
from algorithms import astar, gbfs
from grid import make_grid, generate_maze
from panel import ControlPanel
from canvas import GridCanvas


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("pathfinding agent")
        self.root.configure(bg="#0a0e1a")
        self.root.geometry("1050x650")

        self.rows = tk.IntVar(value=18)
        self.cols = tk.IntVar(value=28)
        self.density = tk.DoubleVar(value=0.28)
        self.algo = tk.StringVar(value="astar")
        self.heur = tk.StringVar(value="manhattan")
        self.dyn_mode = tk.BooleanVar(value=False)
        self.paint = tk.StringVar(value="wall")

        self.start_c = (2, 2)
        self.goal_c = (15, 25)
        self.running = False
        self.v_vis = set()
        self.v_fron = set()
        self.v_path = set()
        self.agent = None
        self.a_path = []
        self.a_idx = 0
        self.anim_id = None
        self.dyn_id = None

        self.grid = make_grid(self.rows.get(), self.cols.get())

        self._shared_state = {
            "rows": self.rows, "cols": self.cols,
            "start_c": self.start_c, "goal_c": self.goal_c,
            "grid": self.grid,
            "v_vis": self.v_vis, "v_fron": self.v_fron, "v_path": self.v_path,
            "agent": self.agent, "running": self.running,
        }

        self._build_ui()
        self._sync_state()
        self.grid_canvas.draw()

    def _sync_state(self):
        self._shared_state.update({
            "start_c": self.start_c,
            "goal_c": self.goal_c,
            "grid": self.grid,
            "v_vis": self.v_vis,
            "v_fron": self.v_fron,
            "v_path": self.v_path,
            "agent": self.agent,
            "running": self.running,
        })

    def _build_ui(self):
        left = tk.Frame(self.root, bg="#111827", width=230)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        callbacks = {
            "apply_size": self.apply_size,
            "generate": self.generate,
            "clear": self.clear,
            "paint_cell": self.paint_cell,
        }

        self.panel = ControlPanel(left, {
            "rows": self.rows, "cols": self.cols,
            "density": self.density, "algo": self.algo,
            "heur": self.heur, "dyn_mode": self.dyn_mode, "paint": self.paint,
        }, callbacks)

        right = tk.Frame(self.root, bg="#0a0e1a")
        right.pack(side="left", fill="both", expand=True)

        self.run_btn = tk.Button(
            right, text="▶  run search", bg="#6366f1", fg="white", bd=0,
            font=("courier", 12, "bold"), padx=26, pady=8, cursor="hand2",
            command=self.toggle_run,
        )
        self.run_btn.pack(pady=(12, 4))

        self.status = tk.Label(
            right, text="draw walls or generate maze, then run.",
            bg="#0a0e1a", fg="#64748b", font=("courier", 9),
        )
        self.status.pack()

        self.grid_canvas = GridCanvas(right, self._shared_state, callbacks)

    def _draw(self):
        self._sync_state()
        self.grid_canvas.draw()

    def apply_size(self):
        self.stop()
        self.grid = make_grid(self.rows.get(), self.cols.get())
        self._clear_vis()
        self._draw()

    def generate(self):
        self.stop()
        d = self.density.get()
        self.grid = generate_maze(self.rows.get(), self.cols.get(), d, self.start_c, self.goal_c)
        self._clear_vis()
        self._draw()
        self.status.config(text=f"maze generated ({int(d * 100)}% walls).")

    def clear(self):
        self.stop()
        self.grid = make_grid(self.rows.get(), self.cols.get())
        self._clear_vis()
        self._draw()

    def _clear_vis(self):
        self.v_vis = set()
        self.v_fron = set()
        self.v_path = set()
        self.agent = None

    def paint_cell(self, cell):
        r, c = cell
        mode = self.paint.get()
        if mode == "start":
            self.start_c = (r, c)
            self.grid[r][c] = empty
        elif mode == "goal":
            self.goal_c = (r, c)
            self.grid[r][c] = empty
        elif mode == "wall" and (r, c) not in (self.start_c, self.goal_c):
            self.grid[r][c] = wall
        elif mode == "erase" and (r, c) not in (self.start_c, self.goal_c):
            self.grid[r][c] = empty
        self._clear_vis()
        self._draw()

    def toggle_run(self):
        if self.running:
            self.stop()
            self.status.config(text="stopped.")
        else:
            self._run_search()

    def _run_search(self):
        self.stop()
        self._clear_vis()
        self._draw()
        self.running = True
        self.run_btn.config(text="⏹  stop", bg="#ef4444")
        self.status.config(text="searching…")
        h = manhattan if self.heur.get() == "manhattan" else euclidean
        fn = astar if self.algo.get() == "astar" else gbfs
        g = [row[:] for row in self.grid]
        threading.Thread(
            target=lambda: self.root.after(
                0, lambda: self._animate(
                    fn(g, self.start_c, self.goal_c, h, self.rows.get(), self.cols.get())
                )
            ),
            daemon=True,
        ).start()

    def _animate(self, res):
        if not self.running:
            return

        if not res["found"]:
            self.panel.update_metrics(len(res["visited"]), "—", res["time"])
            self.status.config(text="no path found.")
            self.running = False
            self.run_btn.config(text="▶  run search", bg="#6366f1")
            return

        vis, fron, path, idx = res["visited"], res["frontier"], res["path"], [0]

        def step():
            if not self.running:
                return
            i = idx[0]
            if i < len(vis):
                self.v_vis.add(vis[i])
                if i < len(fron):
                    self.v_fron.add(fron[i])
                self._draw()
                idx[0] += 1
                self.anim_id = self.root.after(10, step)
            else:
                self.v_fron.clear()
                self.v_path = set(path)
                self._draw()
                self.panel.update_metrics(len(vis), res["cost"], res["time"])
                self.status.config(text=f"path found!  {len(path) - 1} steps.")
                if self.dyn_mode.get():
                    self._start_dynamic(path)
                else:
                    self.running = False
                    self.run_btn.config(text="▶  run search", bg="#6366f1")

        step()

    def _start_dynamic(self, path):
        self.a_path = list(path)
        self.a_idx = 0
        self.agent = path[0]
        self._draw()
        self._dyn_step()

    def _dyn_step(self):
        if not self.running:
            return
        self.a_idx += 1
        if self.a_idx >= len(self.a_path):
            self.agent = None
            self._draw()
            self.status.config(text="agent reached the goal!")
            self.running = False
            self.run_btn.config(text="▶  run search", bg="#6366f1")
            return

        self.agent = self.a_path[self.a_idx]
        self._draw()

        if random.random() < 0.20:
            r = random.randint(0, self.rows.get() - 1)
            c = random.randint(0, self.cols.get() - 1)
            if (r, c) not in (self.start_c, self.goal_c, self.agent) and self.grid[r][c] == empty:
                self.grid[r][c] = wall
                if (r, c) in self.a_path[self.a_idx:]:
                    self.status.config(text="obstacle detected — replanning…")
                    self._replan()
                    return

        self.dyn_id = self.root.after(230, self._dyn_step)

    def _replan(self):
        h = manhattan if self.heur.get() == "manhattan" else euclidean
        fn = astar if self.algo.get() == "astar" else gbfs
        res = fn(self.grid, self.agent, self.goal_c, h, self.rows.get(), self.cols.get())
        if res["found"]:
            self.a_path = res["path"]
            self.a_idx = 0
            self.v_path = set(res["path"])
            self._draw()
            self.panel.update_metrics(len(res["visited"]), res["cost"], res["time"])
            self.status.config(text="replanned successfully.")
            self.dyn_id = self.root.after(230, self._dyn_step)
        else:
            self.status.config(text="no path after obstacle — agent stuck.")
            self.running = False
            self.run_btn.config(text="▶  run search", bg="#6366f1")

    def stop(self):
        self.running = False
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None
        if self.dyn_id:
            self.root.after_cancel(self.dyn_id)
            self.dyn_id = None
        self.run_btn.config(text="▶  run search", bg="#6366f1")
