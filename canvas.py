import tkinter as tk

from constants import clr, wall, empty


class GridCanvas:
    def __init__(self, parent, state, callbacks):
        self.state = state
        self.callbacks = callbacks
        self.cs = 26

        self.canvas = tk.Canvas(
            parent, bg="#0d1117", highlightthickness=2,
            highlightbackground="#1f2937", cursor="crosshair",
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=8)
        self.canvas.bind("<ButtonPress-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)

    def cell_color(self, r, c):
        agent = self.state["agent"]
        start = self.state["start_c"]
        goal = self.state["goal_c"]
        grid = self.state["grid"]
        v_path = self.state["v_path"]
        v_vis = self.state["v_vis"]
        v_fron = self.state["v_fron"]

        if agent == (r, c):
            return clr["agent"]
        if (r, c) == start:
            return clr["start"]
        if (r, c) == goal:
            return clr["goal"]
        if grid[r][c] == wall:
            return clr["wall"]
        if (r, c) in v_path:
            return clr["path"]
        if (r, c) in v_vis:
            return clr["visited"]
        if (r, c) in v_fron:
            return clr["frontier"]
        return clr["empty"]

    def draw(self):
        cs = self.cs
        rows = self.state["rows"].get()
        cols = self.state["cols"].get()
        start = self.state["start_c"]
        goal = self.state["goal_c"]

        self.canvas.delete("all")
        for r in range(rows):
            for c in range(cols):
                x1 = c * (cs + 1) + 2
                y1 = r * (cs + 1) + 2
                self.canvas.create_rectangle(
                    x1, y1, x1 + cs, y1 + cs,
                    fill=self.cell_color(r, c),
                    outline="#0d1117", width=1,
                )
                if (r, c) == start:
                    self.canvas.create_text(
                        x1 + cs // 2, y1 + cs // 2, text="S",
                        fill="white", font=("courier", max(7, cs // 3), "bold"),
                    )
                elif (r, c) == goal:
                    self.canvas.create_text(
                        x1 + cs // 2, y1 + cs // 2, text="G",
                        fill="white", font=("courier", max(7, cs // 3), "bold"),
                    )
        self.canvas.configure(scrollregion=(0, 0, cols * (cs + 1) + 4, rows * (cs + 1) + 4))

    def _to_cell(self, event):
        cs = self.cs
        c = int(event.x // (cs + 1))
        r = int(event.y // (cs + 1))
        rows = self.state["rows"].get()
        cols = self.state["cols"].get()
        return (r, c) if 0 <= r < rows and 0 <= c < cols else None

    def _on_click(self, event):
        if not self.state["running"]:
            cell = self._to_cell(event)
            if cell:
                self.callbacks["paint_cell"](cell)

    def _on_drag(self, event):
        if not self.state["running"]:
            cell = self._to_cell(event)
            if cell:
                self.callbacks["paint_cell"](cell)
